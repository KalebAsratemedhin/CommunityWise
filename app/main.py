"""
FastAPI application - Main entry point.

Your task: Create the FastAPI app with endpoints for:
1. Chat endpoint (POST /chat) - Main interaction
2. Add documents endpoint (POST /documents) - Load new documents
3. Health check (GET /health) - Check if service is running

Hints:
- Use FastAPI's dependency injection for shared resources
- Add proper error handling
- Include API documentation
"""

from app.document_loader import (
    process_documents, 
    process_uploaded_file, 
    validate_file_upload,
    extract_text_from_pdf
)
from app.models import ChatRequest, ChatResponse
from app.rag_engine import initialize_llm, rag_pipeline
from app.vector_store import add_documents_to_vector_store, initialize_vector_store
from app.embeddings import initialize_embedding_model
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
import uuid
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Import your modules (uncomment as you implement them)
# from app.models import ChatRequest, ChatResponse
# from app.rag_engine import initialize_llm, rag_pipeline
# from app.vector_store import initialize_vector_store
# from app.embeddings import initialize_embedding_model
# from app.document_loader import process_documents

load_dotenv()

app = FastAPI(
    title="RAG Chat Bot",
    description="A simple RAG (Retrieval-Augmented Generation) chat bot",
    version="1.0.0"
)

# CORS middleware (allows frontend to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for shared resources
vector_store_collection = None
embedding_model = None
llm_client = None

@app.on_event("startup")
async def startup_event():
    """
    Initialize resources when the app starts.
    """
    global vector_store_collection, embedding_model, llm_client
    
    # TODO: Implement startup initialization
    # 1. Initialize vector store
    # 2. Initialize embedding model
    # 3. Initialize LLM client
    # 4. Load existing documents if any
    client, vector_store_collection = initialize_vector_store()
    embedding_model = initialize_embedding_model()
    llm_client = initialize_llm()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Main chat endpoint.
    
    Receives a user query and returns a RAG-generated response.
    Automatically generates a conversation_id for tracking.
    """
    try:
        # Generate a unique conversation ID for this chat session
        conversation_id = str(uuid.uuid4())
        
        response = rag_pipeline(
            request.message, 
            vector_store_collection, 
            embedding_model, 
            llm_client
        )
        return ChatResponse(
            response=response["response"], 
            sources=response["sources"],
            conversation_id=conversation_id,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/documents")
async def add_documents(directory: str = "data/documents"):
    """
    Load and process documents from a directory.
    
    This will:
    1. Load documents from the specified directory
    2. Split them into chunks
    3. Generate embeddings
    4. Add them to the vector store
    """
    try:
        documents = process_documents(directory)
        if not documents:
            return {"message": "No documents found to process", "count": 0}
        add_documents_to_vector_store(documents, vector_store_collection, embedding_model)
        return {"message": f"Successfully added {len(documents)} document chunks", "count": len(documents)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/documents/upload")
async def upload_documents(file: UploadFile = File(...)):
    """
    Upload a document to the server.
    
    This will:
    1. Validate the uploaded file (size, type)
    2. Read the file content
    3. Extract text (for PDFs, extract from all pages)
    4. Process it into chunks
    5. Generate embeddings
    6. Add to the vector store
    
    Supported file types:
    - .txt, .md: Plain text files
    - .pdf: PDF documents (text extraction from all pages)
    - .docx: Not yet implemented
    
    Maximum file size: 10MB
    """
    try:
        # Read file content first (needed to get size and content)
        content = await file.read()
        file_size = len(content)
        
        # Validate file
        is_valid, error_message = validate_file_upload(
            filename=file.filename,
            file_size=file_size
        )
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_message)
        
        # Decode content based on file type
        file_ext = Path(file.filename).suffix.lower()
        if file_ext == '.txt' or file_ext == '.md':
            # Text files - decode as UTF-8
            try:
                file_content = content.decode('utf-8')
            except UnicodeDecodeError:
                raise HTTPException(
                    status_code=400, 
                    detail="File encoding error. Please ensure the file is UTF-8 encoded."
                )
        elif file_ext == '.pdf':
            # PDF files - extract text using PyPDF2
            try:
                file_content = extract_text_from_pdf(content)
            except ImportError:
                raise HTTPException(
                    status_code=500,
                    detail="PDF processing library (PyPDF2) is not installed. Please install it with: pip install PyPDF2"
                )
            except ValueError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"PDF processing error: {str(e)}"
                )
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Unexpected error processing PDF: {str(e)}"
                )
        elif file_ext == '.docx':
            # DOCX files - would need python-docx
            # For now, raise an error indicating it's not implemented
            raise HTTPException(
                status_code=501,
                detail="DOCX support is not yet implemented. Please convert to .txt or .md format."
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}"
            )
        
        # Process the file content into chunks
        documents = process_uploaded_file(
            file_content=file_content,
            filename=file.filename,
            chunk_size=1000,
            chunk_overlap=200
        )
        
        if not documents:
            raise HTTPException(
                status_code=400,
                detail="No content could be extracted from the file"
            )
        
        # Add to vector store
        add_documents_to_vector_store(documents, vector_store_collection, embedding_model)
        
        return {
            "message": f"Successfully processed and added {len(documents)} document chunks",
            "filename": file.filename,
            "chunks_count": len(documents)
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors, etc.)
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing uploaded file: {str(e)}"
        )

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "RAG Chat Bot API",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)







