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
    # Format context with better structure and source information
    context_parts = []
    for idx, chunk in enumerate(context_chunks, 1):
        metadata = chunk.get("metadata", {})
        source = metadata.get("source", "unknown")
        content_type = metadata.get("type", "document")
        
        # Format based on content type with clear labels
        if content_type == "qa_pair":
            context_parts.append(f"[Q&A Information]\n{chunk['content']}")
        elif content_type == "question":
            context_parts.append(f"[Question]\n{chunk['content']}")
        elif content_type == "answer":
            context_parts.append(f"[Answer]\n{chunk['content']}")
        else:
            context_parts.append(f"[Document: {source}]\n{chunk['content']}")
    
    context_text = "\n\n---\n\n".join(context_parts)

    if use_system_message:
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant that answers questions using the provided context. "
                    "The context contains relevant information from documents and Q&A discussions. "
                    "Your task is to extract and synthesize information from the context to answer the user's question. "
                    "If the context mentions places, recommendations, or answers related to the question, provide that information. "
                    "Be helpful and extract all relevant details from the context, even if they're phrased differently than the question."
                    "If you don't have the information, say: "
                    "'I don't have that information in my knowledge base.'\n\n"
                ),
                ("human", "Context:\n{context}\n\nUser Question: {question}\n\nProvide a helpful answer based on the context above:"),
            ]
        )
    else:
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "human",
                    "You are a helpful assistant. Use the following context to answer the user's question. "
                    "The context may contain Q&A discussions, documents, or other relevant information. "
                    "Extract and provide all relevant information from the context that helps answer the question.\n\n"
                    "Context:\n{context}\n\n"
                    "User Question: {question}\n\n"
                    "Answer based on the context:",
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


