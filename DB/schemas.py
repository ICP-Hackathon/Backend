from pydantic import BaseModel
from typing import List, Optional
from datetime import time

# UserTable 스키마
class UserTableBase(BaseModel):
    userid: str
    name: Optional[str] = '0.0'
    profileimage: Optional[str] = None

class UserTableCreate(BaseModel):
    userid: str

class UserTableUpdate(BaseModel):
    name: Optional[str] = None
    profileimage: Optional[str] = None

# AITable 스키마
class AITableBase(BaseModel):
    id: str
    name: Optional[str] = None
    creator: Optional[str] = None
    image: Optional[str] = None
    category: Optional[str] = None
    introductions: Optional[str] = None
    usage: Optional[int] = 0
    total_usage: Optional[int] = 0
    ratio: Optional[float] = 0.1
    collect: Optional[float] = 0

    class Config:
        from_attributes = True

class AITableCreate(BaseModel):
    name: Optional[str] = None
    creator: Optional[str] = None
    image: Optional[str] = None
    category: Optional[str] = None
    introductions: Optional[str] = None
    contents: Optional[str] = None
    logs: Optional[str] = None

class AITableUserUpdateInput(BaseModel):
    image: Optional[str] = None
    category: Optional[str] = None
    introductions: Optional[str] = None
    contents: Optional[str] = None
    logs: Optional[str] = None

class AITableUserUpdate(BaseModel):
    category: Optional[str] = None
    introductions: Optional[str] = None
    contents: Optional[str] = None
    logs: Optional[str] = None

class AITableUsageUpdate(BaseModel):
    usage: Optional[int] = 0
    total_usage: Optional[int] = 0
    collect: Optional[float] = 0

class AITableCollectUpdate(BaseModel):
    collect: Optional[float] = 0

class AITableListOut(BaseModel):
    ais: List[AITableBase]

    class Config:
        from_attributes = True

# AILogTable 스키마
class AILogTableBase(BaseModel):
    id: int
    aiid: Optional[str] = None
    createdat: Optional[time] = None
    log: Optional[str] = None
    txurl: Optional[str] = None
    faissid: Optional[str] = None
    

class AILogTableCreate(BaseModel):
    aiid: Optional[str] = None
    log: Optional[str] = None
    txurl: Optional[str] = None
    faissid: Optional[str] = None

class AILogTableListOut(BaseModel):
    logs: List[AILogTableBase]

    class Config:
        from_attributes = True
# ChatTable 스키마
class ChatTableBase(BaseModel):
    chatid: str
    aiid: Optional[str] = None
    userid: Optional[str] = None
    
    class Config:
        from_attributes = True

class ChatTableCreate(BaseModel):
    aiid: Optional[str] = None
    userid: Optional[str] = None

class ChatTableListOut(BaseModel):
    chats: List[ChatTableBase]

    class Config:
        from_attributes = True

# ChatContentsTable 스키마
class ChatContentsTableBase(BaseModel):
    chatcontentsid: str
    chatid: Optional[str] = None
    createdat: Optional[time] = None
    senderid: Optional[str] = None
    message: Optional[str] = None
    class Config:
        from_attributes = True

class ChatContentsTableCreateInput(BaseModel):
    senderid: Optional[str] = None
    message: Optional[str] = None

class ChatContentsTableCreate(BaseModel):
    chatcontentsid: str
    chatid: Optional[str] = None
    senderid: Optional[str] = None
    message: Optional[str] = None

class ChatContentsTableListOut(BaseModel):
    chats: List[ChatContentsTableBase]

    class Config:
        from_attributes = True
