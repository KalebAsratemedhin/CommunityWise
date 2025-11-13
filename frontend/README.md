# RAG Chat Bot - Frontend

Modern Next.js chat interface for the RAG Chat Bot.

## Features

- 🎨 Modern UI with shadcn/ui components
- 💬 ChatGPT-like chat interface
- 🔄 RTK Query for efficient API calls
- 📱 Responsive design

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure API URL (optional):
```bash
cp .env.local.example .env.local
# Edit .env.local and set NEXT_PUBLIC_API_URL if your backend runs on a different port
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at [http://localhost:3000](http://localhost:3000)

## Make sure the backend is running

The frontend expects the FastAPI backend to be running on `http://localhost:8000` by default.

Start the backend:
```bash
cd ..
source venv/bin/activate
uvicorn app.main:app --reload
```

## Tech Stack

- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - UI components
- **RTK Query** - Data fetching and caching
- **Redux Toolkit** - State management
