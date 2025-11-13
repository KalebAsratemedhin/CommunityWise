"""
Pydantic models for API request/response validation.

Your task: Define the data models for:
1. Chat messages (user queries)
2. Chat responses (bot replies)
3. Document upload requests
4. Any other API models you need

Hints:
- Use Pydantic BaseModel
- Add field validators if needed
- Consider adding example values for API docs
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# TODO: Create a ChatMessage model
# Should have: message (str), timestamp (optional), role (user/bot)
class ChatMessage(BaseModel):
    """Represents a single chat message."""
    message: str
    timestamp: Optional[datetime] = None
    role: str = Field(default="user")

# TODO: Create a ChatRequest model
# Should have: message (str), conversation_id is auto-generated
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    

# TODO: Create a ChatResponse model
# Should have: response (str), sources (list of document references), timestamp, conversation_id
class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    sources: List[str] = []
    conversation_id: str
    timestamp: Optional[datetime] = None

# TODO: Create a DocumentUpload model (if needed)
class DocumentUpload(BaseModel):
    """Model for document upload requests."""
    file_path: str
    chunk_size: int = 1000
    chunk_overlap: int = 200






