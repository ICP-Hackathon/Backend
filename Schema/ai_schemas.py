from pydantic import BaseModel
from typing import List, Optional
from datetime import time, datetime
from Schema import base_schemas

class AICreate(BaseModel):
    creator_address: str
    name: str
    profile_image_url: str
    category: str
    introductions: str
    rag_contents: str
    rag_comments: str
    created_at: Optional[datetime] = None 

class AIRead(base_schemas.AI):
    rags: List[base_schemas.RAG]
    chats: List[base_schemas.Chat]
    total_prompt_token_usage: int
    total_completion_token_usage: int
    total_token_usage: int