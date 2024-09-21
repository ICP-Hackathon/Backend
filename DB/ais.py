from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func
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

def get_ai_by_id(db: Session, ai_id: str) -> ai_schemas.AIRead:

    ai_table = db.query(models.AITable).filter(models.AITable.id == ai_id).first()
    rags = db.query(models.RAGTable).filter(models.RAGTable.ai_id == ai_id).all()
    chats = db.query(models.ChatTable).filter(models.ChatTable.ai_id == ai_id).all()

    total_prompt_token_usage = db.query(func.sum(models.ChatMessageTable.prompt_tokens))\
        .join(models.ChatTable, models.ChatMessageTable.chat_id == models.ChatTable.id)\
        .filter(models.ChatTable.ai_id == ai_id)\
        .scalar()
    total_completion_token_usage = db.query(func.sum(models.ChatMessageTable.completion_tokens))\
        .join(models.ChatTable, models.ChatMessageTable.chat_id == models.ChatTable.id)\
        .filter(models.ChatTable.ai_id == ai_id)\
        .scalar()

    total_prompt_token_usage = total_prompt_token_usage or 0
    total_completion_token_usage = total_completion_token_usage or 0

    total_token_usage = total_prompt_token_usage + total_completion_token_usage

    ai = base_schemas.AI.model_validate(ai_table)

    ai_read = ai_schemas.AIRead(
        **ai.model_dump(),
        rags=rags,
        chats=chats,
        total_prompt_token_usage=total_prompt_token_usage,
        total_completion_token_usage=total_completion_token_usage,
        total_token_usage=total_token_usage
    )
    
    return ai_read

def get_ais(db: Session, offset: int, limit: int) -> ai_schemas.AIReadList:
    # AITable에서 offset과 limit을 사용하여 AI 목록을 가져옴
    ais = db.query(models.AITable).offset(offset).limit(limit - offset).all()

    ai_list: List[ai_schemas.AIRead] = []  # 결과를 담을 리스트
    for ai in ais:
        ai_read = get_ai_by_id(db=db, ai_id=ai.id)
        ai_list.append(ai_read)

    return ai_schemas.AIReadList(ais=ai_list)

def get_ais_by_user(db: Session, user_address: str) -> ai_schemas.AIReadList:
    # 유저가 만든 AI 리스트를 가져옵니다
    ais = db.query(models.AITable).filter(models.AITable.creator_address == user_address).all()

    my_ai_list = []
    for ai in ais:
        ai_read = get_ai_by_id(db=db, ai_id=ai.id)
        my_ai_list.append(ai_read)

    return ai_schemas.AIReadList(ais=my_ai_list)

def get_today_ais(db: Session, user_address:str) -> ai_schemas.AIReadList:
    ais = db.query(models.AITable).order_by(models.AITable.created_at.desc()).limit(4).all()

    ai_list = []  # 결과를 담을 리스트
    for ai in ais:
        ai_read = get_ai_by_id(db=db, ai_id=ai.id)
        ai_list.append(ai_read)

    return ai_schemas.AIReadList(ais=ai_list) 

def search_ai_by_name(db: Session, name: str, user_address : str) -> ai_schemas.AIReadList:
    ais = db.query(models.AITable).filter(models.AITable.name.like(f"%{name}%")).all()

    ai_list = []  # 결과를 담을 리스트
    for ai in ais:
        ai_read = get_ai_by_id(db=db, ai_id=ai.id)
        ai_list.append(ai_read)

    # 최종 결과로 AIOVerviewList 반환
    return ai_schemas.AIReadList(ais=ai_list) 

def update_ai(db: Session, ai_update: ai_schemas.AIUpdate) -> ai_schemas.AIRead:
    db.query(models.AITable).filter(models.AITable.id == ai_update.id).update({
    models.AITable.name: ai_update.name,
    models.AITable.profile_image_url: ai_update.profile_image_url,
    models.AITable.category: ai_update.category,
    models.AITable.introductions: ai_update.introductions,
    })
    db.commit()
    return get_ai_by_id(db=db, ai_id=ai_update.id)

def delete_ai(db: Session, ai_id: str) -> base_schemas.AI:
    db_ai = db.query(models.AITable).filter(models.AITable.id == ai_id).first()
    if db_ai:
        db.delete(db_ai)
        db.commit()
    return db_ai
