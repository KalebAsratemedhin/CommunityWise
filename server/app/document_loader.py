"""
Document loading and processing module.

Your task: Implement functions to:
1. Load text files from a directory
2. Split documents into chunks
3. Handle different file formats (txt, pdf, docx)

Key concepts:
- Chunking: Breaking large documents into smaller pieces
- Overlap: Keeping some text overlap between chunks to maintain context
- Metadata: Storing information about where each chunk came from

Hints:
- Use LangChain's text splitter (RecursiveCharacterTextSplitter)
- Or implement your own simple splitter
- Store metadata with each chunk (filename, chunk index, etc.)
"""

from typing import List, Dict, Optional, Tuple
from pathlib import Path
import os
from io import BytesIO
try:
    from PyPDF2 import PdfReader
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False


def load_text_file(file_path: str) -> str:
    """
    Load a text file and return its content.
    
    Args:
        file_path: Path to the text file
        
    Returns:
        Content of the file as a string
    """
    # TODO: Implement this function
    # Hint: Use Path(file_path).read_text() or open()
    # pass
    with open(file_path, 'r') as file:
        return file.read()


def load_documents_from_directory(directory: str) -> List[Dict[str, str]]:
    """
    Load all text files from a directory.
    
    Args:
        directory: Path to directory containing documents
        
    Returns:
        List of dictionaries with 'content' and 'metadata' keys
    """
    # TODO: Implement this function
    # Hint: Use Path(directory).glob("*.txt") to find files
    # Return format: [{"content": "...", "metadata": {"source": "file.txt"}}, ...]
    documents = []
    for file in Path(directory).glob("*.txt"):
        documents.append({
            "content": load_text_file(str(file)),
            "metadata": {
                "source": str(file.name)
            }
        })
    return documents

def split_text_into_chunks(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[str]:
    """
    Split text into chunks with overlap.
    
    Args:
        text: The text to split
        chunk_size: Maximum size of each chunk (in characters)
        chunk_overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    # TODO: Implement this function
    # Option 1: Simple implementation - split by characters
    # Option 2: Use LangChain's RecursiveCharacterTextSplitter
    # 
    # Simple approach:
    # - Start at position 0
    # - Take chunk_size characters
    # - Move forward by (chunk_size - chunk_overlap)
    # - Repeat until end of text
    # pass
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - chunk_overlap
    return chunks


def process_documents(
    directory: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[Dict[str, any]]:
    """
    Load and process all documents from a directory.
    
    Args:
        directory: Path to directory containing documents
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of document chunks with metadata
    """
    # TODO: Implement this function
    # This should:
    # 1. Load all documents from directory
    # 2. Split each document into chunks
    # 3. Add metadata to each chunk (source file, chunk index, etc.)
    # Return format: [{"content": "...", "metadata": {...}}, ...]
    chunks = []
    list_of_documents = load_documents_from_directory(directory)
    for document in list_of_documents:
        document_chunks = split_text_into_chunks(document["content"], chunk_size, chunk_overlap)
        for idx, chunk in enumerate(document_chunks):
            chunks.append({
                "content": chunk,
                "metadata": {
                    **document["metadata"],
                    "chunk_index": idx
                }
            })
    return chunks


def process_uploaded_file(
    file_content: str,
    filename: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[Dict[str, any]]:
    """
    Process an uploaded file content into chunks.
    
    Args:
        file_content: The content of the uploaded file as a string
        filename: Name of the uploaded file
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of document chunks with metadata
    """
    chunks = []
    document_chunks = split_text_into_chunks(file_content, chunk_size, chunk_overlap)
    
    for idx, chunk in enumerate(document_chunks):
        chunks.append({
            "content": chunk,
            "metadata": {
                "source": filename,
                "chunk_index": idx,
                "upload_type": "file_upload"
            }
        })
    
    return chunks


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_bytes: PDF file content as bytes
        
    Returns:
        Extracted text content as a string
        
    Raises:
        ValueError: If PDF cannot be read or is encrypted
    """
    if not PDF_SUPPORT:
        raise ImportError("PyPDF2 is not installed. Install it with: pip install PyPDF2")
    
    try:
        pdf_file = BytesIO(pdf_bytes)
        reader = PdfReader(pdf_file)
        
        # Check if PDF is encrypted
        if reader.is_encrypted:
            raise ValueError("PDF is encrypted and cannot be processed. Please provide an unencrypted PDF.")
        
        # Extract text from all pages
        text_content = []
        for page_num, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text.strip():  # Only add non-empty pages
                    text_content.append(page_text)
            except Exception as e:
                # Log but continue with other pages
                print(f"Warning: Could not extract text from page {page_num + 1}: {str(e)}")
                continue
        
        if not text_content:
            raise ValueError("No text content could be extracted from the PDF. The PDF might contain only images.")
        
        return "\n\n".join(text_content)
        
    except Exception as e:
        raise ValueError(f"Error reading PDF: {str(e)}")


def validate_file_upload(
    filename: Optional[str],
    file_size: int,
    max_size_mb: int = 10
) -> Tuple[bool, Optional[str]]:
    """
    Validate an uploaded file.
    
    Args:
        filename: Name of the file
        file_size: Size of the file in bytes
        max_size_mb: Maximum allowed file size in MB
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if filename exists
    if not filename:
        return False, "Filename is required"
    
    # Check file extension
    allowed_extensions = {'.txt', '.pdf', '.docx', '.md'}
    file_ext = Path(filename).suffix.lower()
    if file_ext not in allowed_extensions:
        return False, f"File type not supported. Allowed types: {', '.join(allowed_extensions)}"
    
    # Check file size (convert MB to bytes)
    max_size_bytes = max_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        return False, f"File size exceeds maximum allowed size of {max_size_mb}MB"
    
    if file_size == 0:
        return False, "File is empty"
    
    return True, None





