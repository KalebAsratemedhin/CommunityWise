# Community Wise (formerly RAG Chat Bot)

A full-featured community knowledge platform built with RAG (Retrieval-Augmented Generation) technology. Community Wise combines AI-powered document search with community Q&A features to help teams and communities build, share, and discover knowledge together.

## What is RAG?

RAG combines **Retrieval** (finding relevant information) with **Augmented Generation** (using that information to generate better responses). This allows the platform to answer questions based on your specific documents rather than just generic training data, making responses more accurate and contextually relevant.

## Features

### 🤖 AI-Powered Chat
- Interactive chat interface powered by RAG technology
- Get instant answers from your uploaded documents
- Conversation history and context-aware responses
- Source citations for transparency

### 📄 Document Management
- Upload and manage your documents securely
- Support for various file formats
- Automatic document indexing for fast search
- Private document storage with S3 integration
- View and manage your document library

### 💬 Community Q&A Platform
- Ask questions to the community
- Answer questions and share knowledge
- Vote on questions and answers
- Accept answers as solutions
- Browse questions and answers in a clean interface

### 👥 User Authentication
- Secure user signup and login
- JWT-based authentication
- Protected routes and user sessions
- User profiles and account management

### 🎨 Modern UI/UX
- Beautiful, responsive design with Next.js 16
- Dark mode support
- Sticky navigation header
- Landing page with feature highlights
- Mobile-friendly interface

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Vector Database**: ChromaDB
- **LLM Integration**: LangChain (supports Gemini and other providers)
- **Authentication**: JWT tokens
- **Storage**: S3-compatible storage for documents

### Frontend
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4 (oklch color format)
- **UI Components**: shadcn/ui
- **State Management**: Redux Toolkit Query
- **Fonts**: Geist Sans, Geist Mono, Dancing Script

## Project Structure

```
RAG-chat-bot/
├── server/                   # Backend (FastAPI)
│   ├── app/
│   │   ├── api/routes/       # API endpoints
│   │   │   ├── auth.py       # Authentication routes
│   │   │   ├── chat.py       # RAG chat endpoints
│   │   │   ├── documents.py  # Document management
│   │   │   ├── questions.py  # Q&A platform endpoints
│   │   │   └── health.py     # Health check
│   │   ├── core/             # Core functionality
│   │   │   ├── config.py     # Configuration
│   │   │   ├── database.py   # Database setup
│   │   │   ├── deps.py       # Dependency injection
│   │   │   └── security.py   # Authentication & security
│   │   ├── infra/            # Infrastructure
│   │   │   ├── rag_engine.py # Core RAG logic
│   │   │   ├── embeddings.py # Text embeddings
│   │   │   ├── vector_store.py # Vector database
│   │   │   └── document_loader.py # Document processing
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   └── main.py           # FastAPI application
│   ├── data/documents/       # Sample documents
│   ├── vector_db/            # ChromaDB storage
│   └── requirements.txt      # Python dependencies
├── frontend/                 # Frontend (Next.js)
│   ├── app/                  # Next.js app directory
│   │   ├── page.tsx          # Landing page
│   │   ├── chat/             # Chat interface
│   │   ├── questions/        # Q&A platform
│   │   ├── login/            # Login page
│   │   ├── signup/           # Signup page
│   │   ├── about/            # About page
│   │   ├── privacy/          # Privacy policy
│   │   └── terms/            # Terms of service
│   ├── components/           # React components
│   │   ├── ui/               # shadcn/ui components
│   │   ├── chat/             # Chat components
│   │   ├── questions/        # Q&A components
│   │   ├── documents/        # Document management
│   │   └── auth/             # Authentication components
│   └── lib/                  # Utilities & API
│       ├── api/              # RTK Query API slices
│       ├── store.ts          # Redux store
│       └── app-name.ts       # App name utilities
├── docker-compose.yml        # PostgreSQL setup
└── README.md                 # This file
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (or use Docker Compose)
- S3-compatible storage (or configure for local storage)

### 1. Backend Setup

#### Install Dependencies

```bash
cd server
pip install -r requirements.txt
```

#### Configure Environment

Create a `.env` file in the `server/` directory:

```bash
# Database
DATABASE_URL=postgresql://rag_user:rag_password@localhost:5432/rag_chat

# LLM Provider (Gemini example)
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash-lite

# JWT
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# S3 Storage (or configure for local storage)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your_bucket_name
```

#### Database Setup

Using Docker Compose (recommended):

```bash
docker-compose up -d
```

Or use your own PostgreSQL instance.

#### Initialize Database

```bash
cd server
# Run database migrations (if using Alembic) or create tables
python -c "from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

#### Run the Backend

```bash
cd server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### 2. Frontend Setup

#### Install Dependencies

```bash
cd frontend
npm install
```

#### Configure Environment

Create a `.env.local` file in the `frontend/` directory:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=CommunityWise
```

#### Run the Frontend

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`

**Note**: Make sure the backend is running before using the frontend.

## Usage

### Getting Started

1. **Sign Up**: Create a new account on the landing page
2. **Upload Documents**: Navigate to the chat interface and upload your documents
3. **Ask Questions**: Use the chat interface to ask questions about your documents
4. **Join Q&A**: Browse and participate in the community Q&A platform

### Key Features

- **Chat Interface**: Ask questions and get AI-powered answers from your documents
- **Document Library**: Upload, view, and manage your documents
- **Q&A Platform**: Ask questions, provide answers, and vote on content
- **User Profile**: Manage your account and view your activity

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user info

### Chat
- `POST /api/chat/` - Send message and get RAG response

### Documents
- `GET /api/documents/list` - List uploaded documents
- `POST /api/documents/upload` - Upload a document
- `POST /api/documents/index` - Index a document for RAG
- `GET /api/documents/indexed` - List indexed documents
- `DELETE /api/documents/indexed/{doc_id}` - Delete indexed document

### Questions & Answers
- `GET /api/questions/` - List all questions
- `POST /api/questions/` - Create a question
- `GET /api/questions/{id}` - Get question details
- `PUT /api/questions/{id}` - Update a question
- `DELETE /api/questions/{id}` - Delete a question
- `POST /api/questions/{id}/answers` - Add an answer
- `PUT /api/answers/{id}` - Update an answer
- `DELETE /api/answers/{id}` - Delete an answer
- `POST /api/answers/{id}/accept` - Accept an answer
- `POST /api/votes` - Vote on questions/answers

## Development

### Backend Development

The backend uses FastAPI with SQLAlchemy for database operations and LangChain for RAG functionality.

Key concepts:
- **Chunking**: Documents are split into smaller chunks for better retrieval
- **Embeddings**: Text is converted to vector embeddings for similarity search
- **Vector Search**: ChromaDB stores and searches document embeddings
- **RAG Pipeline**: Combines retrieval with LLM generation for contextual answers

### Frontend Development

The frontend is built with Next.js 16 using the App Router pattern.

- Components are organized by feature
- RTK Query handles all API calls and caching
- Tailwind CSS v4 provides styling with oklch color format
- shadcn/ui components provide consistent UI elements

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license here]

## Support

For issues and questions, please open an issue on the GitHub repository.

Happy coding! 🚀
