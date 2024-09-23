from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func
from DB import models
from Schema import base_schemas, chat_schemas
from datetime import datetime


def is_ai_liked_by_user(db: Session, user_address: str, ai_id: str) -> bool:
    return db.query(models.LikeTable).filter(
        models.LikeTable.user_address == user_address,
        models.LikeTable.ai_id == ai_id
    ).first() is not None

def create_user_like_ai(db: Session, user_address: str, ai_id: str):
    db_like = models.LikeTable(user_address=user_address, ai_id=ai_id, like=True)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

def delete_user_like_ai(db: Session, user_address: str, ai_id: str):
    like_entry = db.query(models.LikeTable).filter(
        models.LikeTable.user_address == user_address,
        models.LikeTable.ai_id == ai_id
    ).first()

    if like_entry:
        db.delete(like_entry)
        db.commit()
        return True
    return False  # If no like entry was found