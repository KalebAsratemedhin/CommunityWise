"""
Core RAG (Retrieval-Augmented Generation) engine using LangChain.

This implementation uses LangChain for easy model switching.
To switch models, just change the LLM_PROVIDER environment variable:
- "gemini" for Google Gemini
- "openai" for OpenAI GPT
- "anthropic" for Claude
- "ollama" for local models

Key concepts:
- Retrieval: Finding relevant documents
- Augmentation: Adding context to the prompt
- Generation: Using LLM to create response
"""

from typing import List, Dict, Optional
import os
from app.config import settings
from app.vector_store import search_similar_documents
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate


def initialize_llm(provider: Optional[str] = None, api_key: Optional[str] = None) -> BaseChatModel:
    """
    Initialize the LLM client using LangChain.
    
    This function makes it easy to switch between different LLM providers.
    Just change the provider name or environment variable.
    
    Args:
        provider: LLM provider name ("gemini", "openai", "anthropic", "ollama")
                  If None, reads from LLM_PROVIDER env var
        api_key: API key (if None, reads from provider-specific env var)
        
    Returns:
        LangChain LLM instance (unified interface for all providers)
    """
    provider = provider or settings.LLM_PROVIDER.lower()
    
    if provider == "gemini":
        api_key = api_key or settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required. Get your API key from https://makersuite.google.com/app/apikey")
        
        # Get model name from settings
        model_name = settings.GEMINI_MODEL
        
        # Remove "models/" prefix if present (LangChain adds it automatically)
        if model_name.startswith("models/"):
            model_name = model_name.replace("models/", "")
        
        try:
            return ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                temperature=settings.LLM_TEMPERATURE,
                convert_system_message_to_human=True  # Gemini doesn't support system messages
            )
        except Exception as e:
            # If model fails, try fallback models
            fallback_models = ["gemini-1.5-flash-latest", "gemini-pro", "gemini-1.5-pro"]
            error_msg = str(e)
            
            if "not found" in error_msg.lower() or "not supported" in error_msg.lower():
                # Try fallback models
                for fallback in fallback_models:
                    if fallback != model_name:
                        try:
                            print(f"Trying fallback model: {fallback}")
                            return ChatGoogleGenerativeAI(
                                model=fallback,
                                google_api_key=api_key,
                                temperature=settings.LLM_TEMPERATURE,
                                convert_system_message_to_human=True
                            )
                        except:
                            continue
                
                # If all fail, raise with helpful message
                raise ValueError(
                    f"Model '{model_name}' not available. "
                    f"Tried fallbacks: {', '.join(fallback_models)}. "
                    f"Please set GEMINI_MODEL to a valid model name. "
                    f"Original error: {error_msg}"
                )
            else:
                raise
    
    elif provider == "openai":
        api_key = api_key or settings.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=api_key,
            temperature=settings.LLM_TEMPERATURE
        )
    else:
        raise ValueError(f"Unknown LLM provider: {provider}. Choose from: gemini, openai, anthropic, ollama")


def retrieve_relevant_context(
    query: str,
    vector_store_collection,
    embedding_model,
    top_k: int = 3
) -> List[Dict[str, any]]:
    """
    Retrieve relevant document chunks for a query.
    
    Args:
        query: User's query
        vector_store_collection: Vector database collection
        embedding_model: Embedding model
        top_k: Number of chunks to retrieve
        
    Returns:
        List of relevant document chunks
    """
    # TODO: Implement this function
    # Hint: Use the search_similar_documents function from vector_store.py
    # pass
    return search_similar_documents(query, vector_store_collection, embedding_model, top_k)


def format_prompt_with_context(
    query: str,
    context_chunks: List[Dict[str, any]],
    use_system_message: bool = False
) -> List:
    """
    Format the prompt with retrieved context using LangChain's prompt template.
    
    Args:
        query: User's query
        context_chunks: Retrieved document chunks
        use_system_message: Whether to use system message (False for Gemini compatibility)
        
    Returns:
        Formatted messages list (works with all LLM providers)
    """
    context_text = "\n\n".join([chunk["content"] for chunk in context_chunks])
    
    # For Gemini compatibility, combine system instruction into human message
    # For other providers, we can use system messages
    if use_system_message:
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Answer the question based on the following context. If you don't know the answer, say so."),
            ("human", "Context:\n{context}\n\nQuestion: {question}\n\nAnswer:")
        ])
    else:
        # Combine system instruction into human message for Gemini compatibility
        prompt_template = ChatPromptTemplate.from_messages([
            ("human", "You are a helpful assistant. Answer the question based on the following context. If you don't know the answer, say so.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:")
        ])
    
    return prompt_template.format_messages(
        context=context_text,
        question=query
    )


def generate_response(
    prompt_messages,
    llm_client: BaseChatModel,
    temperature: float = 0.7
) -> str:
    """
    Generate a response using LangChain LLM (works with any provider).
    
    Args:
        prompt_messages: Formatted prompt messages (from ChatPromptTemplate)
        llm_client: LangChain LLM instance (any provider)
        temperature: Sampling temperature (0-1)
        
    Returns:
        Generated response text
    """
    # Update temperature if needed (some models need this set at initialization)
    if hasattr(llm_client, 'temperature'):
        llm_client.temperature = temperature
    
    # LangChain's unified interface - works the same for all providers!
    response = llm_client.invoke(prompt_messages)
    
    # Extract text from response (LangChain handles differences between providers)
    return response.content


def rag_pipeline(
    query: str,
    vector_store_collection,
    embedding_model,
    llm_client: BaseChatModel,
    top_k: int = 3,
    temperature: float = 0.7
) -> Dict[str, any]:
    """
    Complete RAG pipeline: Retrieve, Augment, Generate.
    
    This function works with ANY LLM provider thanks to LangChain's unified interface!
    Just change the provider in initialize_llm() and everything else stays the same.
    
    Args:
        query: User's query
        vector_store_collection: Vector database collection
        embedding_model: Embedding model
        llm_client: LangChain LLM instance (any provider)
        top_k: Number of chunks to retrieve
        temperature: Sampling temperature (0-1)
        
    Returns:
        Dictionary with response and sources
    """
    # Step 1: Retrieve relevant context
    context_chunks = retrieve_relevant_context(query, vector_store_collection, embedding_model, top_k)
    
    # Step 2: Format prompt with context (LangChain prompt template)
    prompt_messages = format_prompt_with_context(query, context_chunks)
    
    # Step 3: Generate response (works with any LangChain LLM!)
    response = generate_response(prompt_messages, llm_client, temperature)
    
    # Step 4: Extract unique sources from context chunks
    sources = list(set([chunk.get("metadata", {}).get("source", "unknown") for chunk in context_chunks]))
    
    return {"response": response, "sources": sources}






