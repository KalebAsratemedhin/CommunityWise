from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import HTTPException, UploadFile

from app.core.config import settings
from app.infra.document_loader import (
    process_uploaded_file,
    validate_file_upload,
    extract_text_from_pdf,
)
from app.infra.vector_store import (
    add_documents_to_vector_store,
    list_indexed_documents,
    delete_documents_by_source,
)
from app.schemas.documents import (
    DocumentUploadResponse,
    DocumentIndexResponse,
    DocumentInfo,
    IndexedDocumentInfo,
    IndexedDocumentDeleteResponse,
)
from app.services.storage_service import StorageService


class DocumentService:
    """
    Application-level service for document storage and indexing.

    Responsibilities:
    - Upload files to S3 via StorageService
    - Extract text (txt/md/pdf)
    - Chunk and index documents in the vector store
    - List existing documents in S3
    """

    def __init__(self, storage: StorageService, collection, embedding_model) -> None:
        self._storage = storage
        self._collection = collection
        self._embedding_model = embedding_model

    def list_files(self) -> List[DocumentInfo]:
        """List documents stored in S3 and map them to typed schema."""
        raw_files = self._storage.list_files()
        docs: List[DocumentInfo] = []
        for f in raw_files:
            size = int(f["size"]) if f.get("size") is not None else None
            last_modified = (
                datetime.fromisoformat(f["last_modified"])
                if f.get("last_modified")
                else None
            )
            original_filename = f.get("original_filename") or f["key"].split("/")[-1]
            docs.append(
                DocumentInfo(
                    key=f["key"],
                    size=size,
                    last_modified=last_modified,
                    original_filename=original_filename,
                    signed_url=f.get("signed_url"),
                )
            )
        return docs

    def list_indexed_documents(self) -> List[IndexedDocumentInfo]:
        """
        List documents that have been indexed into the vector store,
        aggregated by their source filename.
        """
        raw_indexed = list_indexed_documents(self._collection)
        indexed_docs: List[IndexedDocumentInfo] = []

        for item in raw_indexed:
            last_indexed_at = (
                datetime.fromisoformat(item["last_indexed_at"])
                if item.get("last_indexed_at")
                else None
            )
            indexed_docs.append(
                IndexedDocumentInfo(
                    source=item["source"],
                    chunks_count=item["chunks_count"],
                    last_indexed_at=last_indexed_at,
                )
            )

        return indexed_docs

    def remove_indexed_document(self, source: str) -> IndexedDocumentDeleteResponse:
        """
        Remove all indexed chunks for a given document source from the vector store.
        """
        deleted_chunks = delete_documents_by_source(self._collection, source)
        return IndexedDocumentDeleteResponse(
            source=source,
            deleted_chunks=deleted_chunks,
        )

    async def upload(self, file: UploadFile) -> DocumentUploadResponse:
        """
        Upload a single document to S3, but do not index it.
        """
        content = await file.read()

        s3_key = self._storage.upload_file_bytes(
            file_bytes=content,
            filename=file.filename,
            content_type=file.content_type or "application/octet-stream",
        )

        file_size = len(content)
        is_valid, error_message = validate_file_upload(
            filename=file.filename, file_size=file_size
        )
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_message)

        return DocumentUploadResponse(
            message="File uploaded successfully",
            filename=file.filename,
            chunks_count=None,
            s3_key=s3_key,
        )

    async def index_uploaded(
        self,
        s3_key: str,
        filename: str | None = None,
    ) -> DocumentIndexResponse:
        """
        Fetch an existing file from S3, extract its text, chunk, and index it.
        """
        content, _, metadata = self._storage.get_file_bytes(s3_key)

        effective_filename = (
            filename or metadata.get("original_filename") or s3_key.split("/")[-1]
        )

        file_size = len(content)
        is_valid, error_message = validate_file_upload(
            filename=effective_filename,
            file_size=file_size,
        )
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_message)

        file_content = self._extract_text_for_indexing(
            content=content,
            filename=effective_filename,
        )

        documents = process_uploaded_file(
            file_content=file_content,
            filename=effective_filename,
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
        )

        if not documents:
            raise HTTPException(
                status_code=400,
                detail="No content could be extracted from the file",
            )

        add_documents_to_vector_store(
            documents,
            self._collection,
            self._embedding_model,
        )

        return DocumentIndexResponse(
            message=f"Successfully indexed {len(documents)} document chunks",
            filename=effective_filename,
            chunks_count=len(documents),
            s3_key=s3_key,
        )

    def _extract_text_for_indexing(self, content: bytes, filename: str) -> str:
        """
        Internal helper to extract text based on file extension.
        """
        file_ext = Path(filename).suffix.lower()

        if file_ext in {".txt", ".md"}:
            try:
                return content.decode("utf-8")
            except UnicodeDecodeError:
                raise HTTPException(
                    status_code=400,
                    detail="File encoding error. Please ensure the file is UTF-8 encoded.",
                )

        if file_ext == ".pdf":
            try:
                return extract_text_from_pdf(content)
            except ImportError:
                raise HTTPException(
                    status_code=500,
                    detail=(
                        "PDF processing library (PyPDF2) is not installed. "
                        "Please install it with: pip install PyPDF2"
                    ),
                )
            except ValueError as exc:
                raise HTTPException(
                    status_code=400,
                    detail=f"PDF processing error: {str(exc)}",
                )
            except Exception as exc:  # pragma: no cover
                raise HTTPException(
                    status_code=500,
                    detail=f"Unexpected error processing PDF: {str(exc)}",
                )

        if file_ext == ".docx":
            raise HTTPException(
                status_code=501,
                detail=(
                    "DOCX support is not yet implemented. "
                    "Please convert to .txt or .md format."
                ),
            )

        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_ext}",
        )


