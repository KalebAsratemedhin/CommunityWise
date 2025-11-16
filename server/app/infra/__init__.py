"""
Infrastructure layer package.

This package contains low-level adapters and integrations:
- Embedding model initialization
- Vector store (ChromaDB) operations
- Document loading and chunking
- S3 storage helpers
- Low-level RAG engine based on LangChain

Higher-level services should depend on these modules via the
`app.services.*` and `app.core.deps` modules, not import boto3,
chromadb, sentence-transformers, etc. directly from routers.
"""


