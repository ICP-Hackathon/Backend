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
    created_at: Optional[datetime] = None 

    class Config:
        from_attributes = True

################# RAG TABLE #################

class RAG(BaseModel):
    id: int
    ai_id: str
    comments: str
    faiss_id: str
    tx_hash: str
    created_at: Optional[datetime] = None 

    class Config:
        from_attributes = True

################# Chat TABLE #################

class Chat(BaseModel):
    id: str
    ai_id: str
    user_address: str
    daily_user_access : bool

    class Config:
        from_attributes = True

################# ChatMessage TABLE #################

class ChatMessage(BaseModel):
    id: str
    chat_id: str
    sender_id: str
    message: str
    prompt_tokens : int = 0
    completion_tokens : int = 0
    created_at: Optional[datetime] = None 

    class Config:
        from_attributes = True

################# Like TABLE #################
class Like(BaseModel):
    like_id: int
    user_address: str
    ai_id: str

    class Config:
        from_attributes = True