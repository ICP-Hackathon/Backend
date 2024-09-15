from pydantic import BaseModel
from typing import List, Optional
from datetime import time, datetime

# UserTable 스키마

class UserTableCreate(BaseModel):
    user_address: str
    nickname: Optional[str] = '0.0'
    image_url: Optional[str] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None


class UserTableBase(BaseModel):
    user_address: str
    nickname: Optional[str] = '0.0'
    image_url: Optional[str] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    creator_id: Optional[str] = None
    consumer_id: Optional[str] = None

# AITable 스키마
class AITableBase(BaseModel):
    ai_id: str
    creator_address: Optional[str] = None
    created_at: Optional[datetime] = None  # Use datetime in Pydantic as well
    name: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    introductions: Optional[str] = None
    chat_counts : Optional[int] = None
    prompt_tokens : Optional[float] = None
    completion_tokens : Optional[float] = None
    weekly_users : Optional[int] = None

    class Config:
        from_attributes = True

class AITableCreate(BaseModel):
    creator_address: Optional[str] = None
    name: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    introductions: Optional[str] = None
    contents: Optional[str] = None
    comments: Optional[str] = None

class AITableOut(BaseModel):
    creator_address: Optional[str] = None
    name: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    introductions: Optional[str] = None
    nickname: Optional[str] = '0.0'
    class Config:
        from_attributes = True

class AITableUserUpdateInput(BaseModel):
    ai_id : Optional[str] = None
    user_address : Optional[str] = None
    name: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    introductions: Optional[str] = None
    contents: Optional[str] = None
    comments: Optional[str] = None

class AITableUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    introductions: Optional[str] = None

class AITableUsageUpdate(BaseModel):
    chat_counts : Optional[int] = None
    prompt_tokens : Optional[float] = None
    completion_tokens : Optional[float] = None
    weekly_users : Optional[int] = None


class AITableListOut(BaseModel):
    ais: List[AITableOut]
    class Config:
        from_attributes = True


# class AITableListOut(BaseModel):
#     ais: List[AITableBase]
#     class Config:
#         from_attributes = True

class AISearch(BaseModel):
    name: Optional[str] = None
    creator_address: Optional[str] = None
    image_url: Optional[str] = None
        
class AISearchListOut(BaseModel):
    ais : List[AISearch]
    class Config:
        from_attributes = True


# AILogTable 스키마

class RAGTableBase(BaseModel):
    rag_id: int
    ai_id: Optional[str] = None
    created_at: Optional[str] = None
    comments: Optional[str] = None
    tx_url: Optional[str] = None
    faiss_id: Optional[str] = None
    class Config:
        from_attributes = True

    

class RAGTableCreate(BaseModel):
    ai_id: Optional[str] = None
    created_at: Optional[str] = None
    comments: Optional[str] = None
    tx_url: Optional[str] = None
    faiss_id: Optional[str] = None

class RAGTableListOut(BaseModel):
    logs: List[RAGTableBase]

    class Config:
        from_attributes = True

class AIDetail(BaseModel):
    ai_id: str
    creator_address: Optional[str] = None
    created_at: Optional[str] = None
    name: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    introductions: Optional[str] = None
    chat_counts : Optional[int] = 0
    prompt_tokens : Optional[float] = 0
    completion_tokens : Optional[float] = 0
    weekly_users : Optional[int] = 0
    logs: List[RAGTableBase]

    class Config:
        from_attributes = True

# ChatTable 스키마
class ChatTableBase(BaseModel):
    chat_id: str
    ai_id: Optional[str] = None
    user_address: Optional[str] = None
    
    class Config:
        from_attributes = True

class ChatTableCreate(BaseModel):
    ai_id: Optional[str] = None
    user_address: Optional[str] = None

class ChatTableListOut(BaseModel):
    chats: List[ChatTableBase]

    class Config:
        from_attributes = True

# ChatContentsTable 스키마
class ChatContentsTableBase(BaseModel):
    chat_contents_id: str
    chat_id: Optional[str] = None
    created_at: Optional[str] = None
    sender_id: Optional[str] = None
    message: Optional[str] = None
    class Config:
        from_attributes = True

class ChatContentsTableCreateInput(BaseModel):
    sender_id: Optional[str] = None
    message: Optional[str] = None

class ChatContentsTableCreate(BaseModel):
    chat_contents_id: str
    chat_id: Optional[str] = None
    sender_id: Optional[str] = None
    message: Optional[str] = None

class ChatContentsTableListOut(BaseModel):
    chats: List[ChatContentsTableBase]

    class Config:
        from_attributes = True
