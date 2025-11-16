"""
Core RAG (Retrieval-Augmented Generation) engine using LangChain.

This module provides low-level primitives:
- Initializing LLM clients (Gemini / OpenAI via LangChain)
- Retrieving relevant context from the vector store
- Building prompts with context
- Invoking the LLM to generate answers

Higher-level orchestration should be done via `services.rag_service.RAGService`.
"""

from typing import List, Dict, Optional, Any

from app.core.config import settings
from app.infra.vector_store import search_similar_documents
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate


def initialize_llm(provider: Optional[str] = None, api_key: Optional[str] = None) -> BaseChatModel:
    """
    Initialize the LLM client using LangChain.

    This function makes it easy to switch between different LLM providers.
    Just change the provider name or environment variable.
    """
    provider = provider or settings.LLM_PROVIDER.lower()

    if provider == "gemini":
        api_key = api_key or settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is required. "
                "Get your API key from https://makersuite.google.com/app/apikey"
            )

        model_name = settings.GEMINI_MODEL
        if model_name.startswith("models/"):
            model_name = model_name.replace("models/", "")

        try:
            return ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                temperature=settings.LLM_TEMPERATURE,
                convert_system_message_to_human=True,
            )
        except Exception as exc:
            fallback_models = ["gemini-1.5-flash-latest", "gemini-pro", "gemini-1.5-pro"]
            error_msg = str(exc)
            if "not found" in error_msg.lower() or "not supported" in error_msg.lower():
                for fallback in fallback_models:
                    if fallback != model_name:
                        try:
                            print(f"Trying fallback model: {fallback}")
                            return ChatGoogleGenerativeAI(
                                model=fallback,
                                google_api_key=api_key,
                                temperature=settings.LLM_TEMPERATURE,
                                convert_system_message_to_human=True,
                            )
                        except Exception:
                            continue
                raise ValueError(
                    f"Model '{model_name}' not available. "
                    f"Tried fallbacks: {', '.join(fallback_models)}. "
                    f"Please set GEMINI_MODEL to a valid model name. "
                    f"Original error: {error_msg}"
                )
            raise

    if provider == "openai":
        api_key = api_key or settings.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=api_key,
            temperature=settings.LLM_TEMPERATURE,
        )

    raise ValueError(f"Unknown LLM provider: {provider}. Choose from: gemini, openai")


def retrieve_relevant_context(
    query: str,
    vector_store_collection: Any,
    embedding_model: Any,
    top_k: int = 3,
) -> List[Dict[str, Any]]:
    """
    Retrieve relevant document chunks for a query from the vector store.
    """
    return search_similar_documents(query, vector_store_collection, embedding_model, top_k)


def format_prompt_with_context(
    query: str,
    context_chunks: List[Dict[str, Any]],
    use_system_message: bool = False,
) -> List[Any]:
    """
    Format the prompt with retrieved context using LangChain's prompt template.
    """
    context_text = "\n\n".join(chunk["content"] for chunk in context_chunks)

    if use_system_message:
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant. Answer the question based on the "
                    "following context. If you don't know the answer, say so.",
                ),
                ("human", "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"),
            ]
        )
    else:
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "human",
                    "You are a helpful assistant. Answer the question based on the "
                    "following context. If you don't know the answer, say so.\n\n"
                    "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:",
                )
            ]
        )

    return prompt_template.format_messages(context=context_text, question=query)


def generate_response(
    prompt_messages: List[Any],
    llm_client: BaseChatModel,
    temperature: float = 0.7,
) -> str:
    """
    Generate a response using the configured LLM via LangChain.
    """
    if hasattr(llm_client, "temperature"):
        llm_client.temperature = temperature

    response = llm_client.invoke(prompt_messages)
    return response.content


def rag_pipeline(
    query: str,
    vector_store_collection: Any,
    embedding_model: Any,
    llm_client: BaseChatModel,
    top_k: int = 3,
    temperature: float = 0.7,
) -> Dict[str, Any]:
    """
    Complete RAG pipeline: retrieve context, build prompt, generate answer.
    """
    context_chunks = retrieve_relevant_context(
        query, vector_store_collection, embedding_model, top_k
    )
    prompt_messages = format_prompt_with_context(query, context_chunks)
    answer = generate_response(prompt_messages, llm_client, temperature)

    sources = list(
        {chunk.get("metadata", {}).get("source", "unknown") for chunk in context_chunks}
    )

    return {"response": answer, "sources": sources}


