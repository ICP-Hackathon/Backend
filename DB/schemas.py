from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

################# USER TABLE #################

class User(BaseModel):
    user_address: str
    nickname: str = '0.0'
    gender: str
    country: str
    interest: str
    profile_image_url: str

    class Config:
        from_attributes = True

class UserList(BaseModel):
    users : List[User]

    class Config:
        from_attributes = True

################# AI TABLE #################

class AI(BaseModel):
    id: str
    creator_address: str
    name: str
    profile_image_url: str
    category: str
    introductions: str
    created_at: datetime

    class Config:
        from_attributes = True

################# RAG TABLE #################

class RAG(BaseModel):
    id: int
    ai_id: str
    comments: str
    faiss_id: str
    tx_hash: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
