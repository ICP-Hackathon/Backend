from pydantic import BaseModel
from typing import List, Optional
from datetime import time, datetime

################# USER TABLE #################

class User(BaseModel):
    user_address: str
    nickname: Optional[str] = '0.0'
    image_url: Optional[str] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    interest: Optional[str] = None
    class Config:
        from_attributes = True

class UserList(BaseModel):
    users : List[User]
    class Config:
        from_attributes = True

################# AI TABLE #################

class AITableBase(BaseModel):
    ai_id: str
    creator_address: Optional[str] = None
    created_at: Optional[datetime] = None  # Use datetime in Pydantic as well
    ai_name: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    introductions: Optional[str] = None

    class Config:
        from_attributes = True

class AIOverview(BaseModel):
    ai_id: str
    creator_address: Optional[str] = None
    image_url: Optional[str] = None
    ai_name: Optional[str] = None
    creator: Optional[str] = None
    category: Optional[str] = None
    like : Optional[bool] = False
    class Config:
        from_attributes = True

class AIOVerviewList(BaseModel):
    ais : List[AIOverview]
    class Config:
        from_attributes = True

class AITableCreate(BaseModel):
    creator_address: Optional[str] = None
    ai_name: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    introductions: Optional[str] = None
    contents: Optional[str] = None
    comments: Optional[str] = None
    
class AITableDelete(BaseModel):
    ai_id: str
    creator_address: str

class AITableUserUpdateInput(AITableBase):
    contents: Optional[str] = None
    comments: Optional[str] = None

class AITableUpdate(BaseModel):
    ai_name: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    introductions: Optional[str] = None


class MyAIsOut(AITableBase):
    usage : Optional[int] = 0

class MyAIsOutList(BaseModel):
    ais : List[MyAIsOut]
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

class AIDetail(AITableBase):
    creator : Optional[str] = None
    chatcount : Optional[int] = None
    usage : Optional[int] = None
    logs: List[RAGTableBase]
    class Config:
        from_attributes = True

# ChatTable 스키마
class ChatTableBase(BaseModel):
    chat_id: str
    ai_id: Optional[str] = None
    user_address: Optional[str] = None
    daily_user_access : Optional[bool] = True
    class Config:
        from_attributes = True

class ChatTableCreate(BaseModel):
    ai_id: Optional[str] = None
    user_address: Optional[str] = None

class ChatTableOverView(BaseModel):
    chat_id : Optional[str] = None
    ai_id : Optional[str] = None
    category : Optional[str] = None
    bool_like : Optional[bool] = False
    creator_address: Optional[str] = None
    image_url: Optional[str] = None
    ai_name: Optional[str] = None
    creator: Optional[str] = None

    class Config:
        from_attributes = True

class ChatTableOverViewList(BaseModel):
    chats : List[ChatTableOverView]
    class Config:
        from_attributes = True    

# ChatContentsTable 스키마
class ChatContentsTableBase(BaseModel):
    chat_contents_id: str
    chat_id: Optional[str] = None
    created_at: Optional[datetime] = None  # Use datetime in Pydantic as well
    sender_id: Optional[str] = None
    message: Optional[str] = None
    prompt_tokens : Optional[int] = 0
    completion_tokens : Optional[int] = 0
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
    prompt_tokens : Optional[int] = 0
    completion_tokens : Optional[int] = 0

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
    ai_name: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    class Config:
        from_attributes = True

class LikedAIList(BaseModel):
    ais : List[LikedAIOut]
    class Config:
        from_attributes = True