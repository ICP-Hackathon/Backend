from typing import List

from sqlalchemy.orm import Session
from DB import models
from Schema import base_schemas, ai_schemas
from datetime import datetime

def check_ai_exists(db: Session, ai_id: str) -> bool:
    return db.query(models.AITable).filter(models.AITable.id == ai_id).first() is not None


def create_ai(db: Session,ai_id:str, ai: ai_schemas.AICreate):
    aiDB = base_schemas.AI(
        id = ai_id,
        creator_address =  ai.creator_address,
        name = ai.name,
        profile_image_url = ai.profile_image_url,
        category = ai.category,
        introductions = ai.introductions,
    )

    db_ai = models.AITable(**aiDB.model_dump())
    db.add(db_ai)
    db.commit()
    db.refresh(db_ai)
    return db_ai