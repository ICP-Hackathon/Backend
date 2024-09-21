from pydantic import BaseModel
from typing import List, Optional
from datetime import time, datetime
from Schema import base_schemas

class ChatCreate(BaseModel):
    ai_id: str
    user_address: str

class ChatRead(base_schemas.Chat):
    ai : base_schemas.AI

class ChatReadList(BaseModel):
    chats : List[ChatRead]

class ChatMessagesRead(base_schemas.Chat):
    ai : base_schemas.AI
    messages : List[base_schemas.ChatMessage]