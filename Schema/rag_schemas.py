from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RAGCreate(BaseModel):
    ai_id: str
    comments: str
    faiss_id: str
    tx_hash: str
    created_at: Optional[datetime] = None 