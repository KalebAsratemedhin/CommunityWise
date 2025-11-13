"""
Vector database operations.

Your task: Implement functions to store and retrieve documents using a vector database.

Key concepts:
- Vector database: Stores embeddings and allows similarity search
- Similarity search: Find documents with similar embeddings to a query
- ChromaDB: Simple, local vector database (recommended)

Hints:
- Use ChromaDB for simplicity
- Store both embeddings and metadata
- Implement add_documents and search_similar functions
"""

from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from app.embeddings import generate_embeddings, generate_embedding
import uuid


def initialize_vector_store(persist_directory: str = "./vector_db"):
    """
    Initialize the vector database.
    
    Args:
        persist_directory: Directory to persist the database
        
    Returns:
        ChromaDB client and collection
    """
    # TODO: Implement this function
    # Hint:
    #   client = chromadb.PersistentClient(path=persist_directory)
    #   collection = client.get_or_create_collection(name="documents")
    #   return client, collection
    # pass
    client = chromadb.PersistentClient(path=persist_directory)
    collection = client.get_or_create_collection(name="documents")
    return client, collection


def add_documents_to_vector_store(
    documents: List[Dict[str, any]],
    collection,
    embedding_model
):
    """
    Add documents to the vector store.
    
    Args:
        documents: List of document chunks with content and metadata
        collection: ChromaDB collection
        embedding_model: Model to generate embeddings
    """
    # TODO: Implement this function
    # Steps:
    # 1. Extract texts from documents
    # 2. Generate embeddings for texts
    # 3. Prepare metadata (convert to dict format)
    # 4. Add to collection using collection.add()
    # 
    # ChromaDB format:
    #   collection.add(
    #       ids=[...],
    #       embeddings=[...],
    #       documents=[...],
    #       metadatas=[...]
    #   )
    # pass
    texts = [doc["content"] for doc in documents]
    embeddings = generate_embeddings(texts, embedding_model)
    # Generate unique UUIDs for each document chunk to avoid collisions
    ids = [str(uuid.uuid4()) for _ in range(len(documents))]
    metadatas = [doc.get("metadata", {}) for doc in documents]
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas
    )


def search_similar_documents(
    query: str,
    collection,
    embedding_model,
    top_k: int = 3
) -> List[Dict[str, any]]:
    """
    Search for similar documents in the vector store.
    
    Args:
        query: Search query text
        collection: ChromaDB collection
        embedding_model: Model to generate embeddings
        top_k: Number of results to return
        
    Returns:
        List of similar documents with metadata
    """
    # TODO: Implement this function
    # Steps:
    # 1. Generate embedding for the query
    # 2. Use collection.query() to search
    # 3. Return results with content and metadata
    #
    # ChromaDB query format:
    #   results = collection.query(
    #       query_embeddings=[query_embedding],
    #       n_results=top_k
    #   )
    # pass
    query_embedding = generate_embedding(query, embedding_model)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    # ChromaDB returns results as dict with lists of lists
    # Format: {"documents": [[doc1, doc2, ...]], "metadatas": [[meta1, meta2, ...]], ...}
    # We need to convert to list of dicts
    formatted_results = []
    if results["documents"] and len(results["documents"]) > 0:
        documents = results["documents"][0]  # First (and only) query result
        metadatas = results["metadatas"][0] if results["metadatas"] else [{}] * len(documents)
        ids = results["ids"][0] if results["ids"] else [None] * len(documents)
        
        for doc, metadata, doc_id in zip(documents, metadatas, ids):
            formatted_results.append({
                "content": doc,
                "metadata": metadata or {},
                "id": doc_id
            })
    
    return formatted_results



