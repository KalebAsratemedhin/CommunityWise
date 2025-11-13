# RAG Chat Bot

A simple but complete RAG (Retrieval-Augmented Generation) chat bot built with Python, FastAPI, and LangChain.

## What is RAG?

RAG combines **Retrieval** (finding relevant information) with **Augmented Generation** (using that information to generate better responses). This allows the chatbot to answer questions based on specific documents rather than just its training data.

## Project Structure

```
RAG-chat-bot/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── rag_engine.py        # Core RAG logic
│   ├── embeddings.py        # Text embeddings
│   ├── vector_store.py      # Vector database
│   └── document_loader.py   # Document processing
├── data/
│   └── documents/           # Place your documents here
├── vector_db/               # Vector database storage
└── requirements.txt
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Add Documents

Place your text files in `data/documents/` directory.

### 4. Run the Application

```bash
python -m app.main
# Or
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

## Learning Path

See `PROJECT_PLAN.md` for a detailed step-by-step guide on how to implement each component.

## Implementation Order

1. **Document Processing** (`document_loader.py`) - Load and chunk documents
2. **Embeddings** (`embeddings.py`) - Convert text to vectors
3. **Vector Store** (`vector_store.py`) - Store and search vectors
4. **RAG Engine** (`rag_engine.py`) - Core RAG pipeline
5. **API** (`main.py`, `models.py`) - FastAPI endpoints

## Testing the API

Once implemented, you can test with:

```bash
# Chat with the bot
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is this document about?"}'

# Add documents
curl -X POST "http://localhost:8000/documents?directory=data/documents"
```

## Key Concepts

- **Chunking**: Breaking documents into smaller pieces
- **Embeddings**: Numerical representations of text
- **Vector Search**: Finding similar documents quickly
- **Prompt Engineering**: Formatting context for the LLM

## Next Steps

1. Read `PROJECT_PLAN.md` for detailed explanations
2. Start implementing `document_loader.py`
3. Work through each module step by step
4. Test as you go!

Happy coding! 🚀
