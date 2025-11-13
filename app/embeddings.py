"""
Text embedding utilities.

Your task: Implement functions to generate embeddings for text.

Key concepts:
- Embeddings: Converting text into numerical vectors
- Similar texts have similar vectors
- Used for semantic search

Options:
1. Sentence Transformers (free, local) - Recommended for learning
2. OpenAI embeddings (paid, but high quality)

Hints:
- Use sentence-transformers library for local embeddings
- Or use OpenAI's embedding API
- Embeddings are typically 384 or 1536 dimensions
"""

from typing import List
from sentence_transformers import SentenceTransformer
import os


def initialize_embedding_model(model_name: str = "all-MiniLM-L6-v2"):
    """
    Initialize the embedding model.
    
    Args:
        model_name: Name of the model to use
        
    Returns:
        The embedding model
    """
    # TODO: Implement this function
    # Option 1: sentence-transformers
    #   from sentence_transformers import SentenceTransformer
    #   return SentenceTransformer(model_name)
    #
    # Option 2: OpenAI (if you prefer)
    #   Just return None and use OpenAI API directly
    # pass
    return SentenceTransformer(model_name)


def generate_embeddings(texts: List[str], model) -> List[List[float]]:
    """
    Generate embeddings for a list of texts.
    
    Args:
        texts: List of text strings to embed
        model: The embedding model (from initialize_embedding_model)
        
    Returns:
        List of embedding vectors (each is a list of floats)
    """
    # TODO: Implement this function
    # If using sentence-transformers:
    #   return model.encode(texts).tolist()
    #
    # If using OpenAI:
    #   Use OpenAI API to get embeddings
    # pass
    return model.encode(texts).tolist()


def generate_embedding(text: str, model) -> List[float]:
    """
    Generate embedding for a single text.
    
    Args:
        text: Text string to embed
        model: The embedding model
        
    Returns:
        Embedding vector as a list of floats
    """
    # TODO: Implement this function
    # Hint: Can call generate_embeddings with a single-item list
    # pass
    return generate_embeddings([text], model)[0]







