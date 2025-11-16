from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    """Response returned when a single document is uploaded (no indexing yet)."""

    message: str
    filename: Optional[str]
    chunks_count: Optional[int] = None
    s3_key: Optional[str]


class DocumentIndexRequest(BaseModel):
    """Request body for indexing an already uploaded document."""

    s3_key: str
    filename: Optional[str] = None


class DocumentIndexResponse(BaseModel):
    """Response returned when an existing document has been indexed."""

    message: str
    filename: Optional[str]
    chunks_count: int
    s3_key: str


class DocumentInfo(BaseModel):
    """Information about a stored document in S3."""

    key: str
    size: Optional[int]
    last_modified: Optional[datetime]
    original_filename: Optional[str] = None
    signed_url: Optional[str] = None


class IndexedDocumentInfo(BaseModel):
    """Aggregated information about an indexed document in the vector store."""

    source: str
    chunks_count: int
    last_indexed_at: Optional[datetime] = None


class IndexedDocumentDeleteResponse(BaseModel):
    """Response returned when indexed chunks for a document are removed."""

    source: str
    deleted_chunks: int

