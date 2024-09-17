from pydantic import BaseModel
from typing import List, Optional
from datetime import time, datetime

################# USER TABLE #################

class UserTableBase(BaseModel):
    user_address: str
    nickname: Optional[str] = '0.0'
    image_url: Optional[str] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    class Config:
        from_attributes = True

class UserTableUpdate(BaseModel):
    user_address: str
    image_url: Optional[str] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    class Config:
        from_attributes = True

class UserTableCreate(UserTableUpdate):
    nickname: Optional[str] = '0.0' 
    pass

class UserTableList(BaseModel):
    users : List[UserTableBase]
    class Config:
        from_attributes = True

################# AI TABLE #################

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

class AIOverview(BaseModel):
    ai_id: str
    creator_address: Optional[str] = None
    name: Optional[str] = None
    creator: Optional[str] = None
    like : Optional[bool] = False
    class Config:
        from_attributes = True

class AIOVerviewList(BaseModel):
    ais : List[AIOverview]
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

class AITableOut(AITableBase):
    creator: Optional[str] = None
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
    created_at: Optional[datetime] = None  # Use datetime in Pydantic as well
    comments: Optional[str] = None
    tx_url: Optional[str] = None
    faiss_id: Optional[str] = None
    class Config:
        from_attributes = True

    

class RAGTableCreate(BaseModel):
    ai_id: Optional[str] = None
    created_at: Optional[datetime] = None  # Use datetime in Pydantic as well
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
    created_at: Optional[datetime] = None  # Use datetime in Pydantic as well
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

class ChatTableOut(AITableBase):
    chat_id: str
    ai_id: Optional[str] = None
    user_address: Optional[str] = None
    
    class Config:
        from_attributes = True

class ChatTableCreate(BaseModel):
    ai_id: Optional[str] = None
    user_address: Optional[str] = None

class ChatTableListOut(BaseModel):
    chats: List[ChatTableOut]

    class Config:
        from_attributes = True

# ChatContentsTable 스키마
class ChatContentsTableBase(BaseModel):
    chat_contents_id: str
    chat_id: Optional[str] = None
    created_at: Optional[datetime] = None  # Use datetime in Pydantic as well
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


##Like Table

# Base schema for LikeTable
class LikeTableBase(BaseModel):
    like_id: int
    user_address: Optional[str] = None
    ai_id: Optional[str] = None

    class Config:
        from_attributes = True

# Schema for creating a Like entry
class LikeTableCreate(BaseModel):
    user_address: str
    ai_id: str

    class Config:
        from_attributes = True

class LikedAIOut(LikeTableBase):
    creator_address: Optional[str] = None
    name: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    class Config:
        from_attributes = True

class LikedAIList(BaseModel):
    ais : List[LikedAIOut]
    class Config:
        from_attributes = True