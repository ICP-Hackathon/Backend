from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func
from DB import models
from Schema import base_schemas, chat_schemas
from datetime import datetime

def check_chat_exists(db: Session, chat_id: str) -> bool:
    return db.query(models.ChatTable).filter(models.ChatTable.id == chat_id).first() is not None

def get_chats_by_user_address(db: Session, user_address: str):
    results = (
        db.query(models.ChatTable, models.AITable)
        .join(models.AITable, models.ChatTable.ai_id == models.AITable.id)
        .filter(models.ChatTable.user_address == user_address)
        .all()
    )

    chats = [
        chat_schemas.ChatRead(
          id=chat.id,
          ai_id=chat.ai_id,
          user_address=chat.user_address,
          ai=ai
        )
        for chat, ai in results
    ]

    return chat_schemas.ChatReadList(chats=chats)

def create_chat(db: Session, chat: base_schemas.Chat):
    db_chat = models.ChatTable(**chat.model_dump())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def create_chat_message(db: Session, chat_message: base_schemas.ChatMessage):
    db_chat_content = models.ChatMessageTable(**chat_message.model_dump())
    db.add(db_chat_content)
    db.commit()
    db.refresh(db_chat_content)
    return db_chat_content