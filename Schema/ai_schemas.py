from pydantic import BaseModel
from typing import List, Optional
from datetime import time, datetime

class AICreate(BaseModel):
    creator_address: str
    name: str
    profile_image_url: str
    category: str
    introductions: str
    rag_contents: str
    rag_comments: str
    created_at: Optional[datetime] = None 