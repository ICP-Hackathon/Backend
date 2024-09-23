from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func
from DB import models
from Schema import base_schemas, chat_schemas
from datetime import datetime


def check_chat_exists(db: Session, chat_id: str) -> bool:
    return db.query(models.ChatTable).filter(models.ChatTable.id == chat_id).first() is not None

def get_chat_by_id(db: Session, chat_id: str) -> base_schemas.Chat:
    chat_model = db.query(models.ChatTable).filter(models.ChatTable.id == chat_id).first()
    chat = base_schemas.Chat.model_validate(chat_model)
    return chat

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
    return chat_message

def get_chat_messages(db: Session, chat_id: str) -> chat_schemas.ChatMessagesRead:
    chat_db = db.query(models.ChatTable).filter(models.ChatTable.id == chat_id).first()
    chat = base_schemas.Chat.model_validate(chat_db)
    messages = db.query(models.ChatMessageTable).filter(models.ChatMessageTable.chat_id == chat_id).all()
    message_list = []
    for message in messages:
        m = base_schemas.ChatMessage.model_validate(message)
        message_list.append(m)
    return chat_schemas.ChatMessagesRead(id=chat.id, ai_id=chat.ai_id, user_address=chat.user_address, messages=message_list)