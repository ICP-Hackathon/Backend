from pydantic import BaseModel
from typing import List, Optional
from datetime import time

# UserTable 스키마
class UserTableBase(BaseModel):
    userid: str
    name: Optional[str] = None
    profileimage: Optional[str] = None

class UserTableCreate(UserTableBase):
    pass

class UserTableUpdate(BaseModel):
    name: Optional[str] = None
    profileimage: Optional[str] = None

class UserTableInDB(UserTableBase):
    pass

class UserTableOut(UserTableInDB):
    pass

# AITable 스키마
class AITableBase(BaseModel):
    id: str
    name: Optional[str] = None
    category: Optional[str] = None
    introductions: Optional[str] = None
    usage: Optional[int] = None
    total_usage: Optional[int] = None
    ratio: Optional[int] = None

class AITableCreate(BaseModel):
    id: str
    name: Optional[str] = None
    category: Optional[str] = None
    introductions: Optional[str] = None

class AITableUserUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    introductions: Optional[str] = None

class AITableInDB(AITableBase):
    pass

class AITableOut(AITableInDB):
    pass

# AILogTable 스키마
class AILogTableBase(BaseModel):
    id: int
    aiid: Optional[str] = None
    createdat: Optional[time] = None
    log: Optional[str] = None
    txurl: Optional[str] = None

class AILogTableCreate(BaseModel):
    aiid: Optional[str] = None
    createdat: Optional[time] = None
    log: Optional[str] = None
    txurl: Optional[str] = None

class AILogTableUpdate(AILogTableBase):
    pass

class AILogTableInDB(AILogTableBase):
    pass

class AILogTableOut(AILogTableInDB):
    class Config:
        from_attributes = True

class AILogTableListOut(BaseModel):
    logs: List[AILogTableOut]

    class Config:
        from_attributes = True
# ChatTable 스키마
class ChatTableBase(BaseModel):
    chatid: str
    aiid: Optional[str] = None
    userid: Optional[str] = None

class ChatTableCreate(ChatTableBase):
    pass

class ChatTableUpdate(ChatTableBase):
    pass

class ChatTableInDB(ChatTableBase):
    pass

class ChatTableOut(ChatTableInDB):
    pass

# ChatContentsTable 스키마
class ChatContentsTableBase(BaseModel):
    chatcontentsid: str
    chatid: Optional[str] = None
    createdat: Optional[time] = None
    senderid: Optional[str] = None
    message: Optional[str] = None
    class Config:
        from_attributes = True

class ChatContentsTableCreate(ChatContentsTableBase):
    pass

class ChatContentsTableUpdate(ChatContentsTableBase):
    pass

class ChatContentsTableInDB(ChatContentsTableBase):
    pass

class ChatContentsTableOut(BaseModel):
    chats: List[ChatContentsTableBase]
    class Config:
        from_attributes = True
    
