from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func
from DB import models
from Schema import base_schemas, ai_schemas
from datetime import datetime
from DB.likes import is_ai_liked_by_user

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

def get_ai_by_id(db: Session, ai_id: str, user_address : str = "") -> ai_schemas.AIRead:

    ai_table = db.query(models.AITable).filter(models.AITable.id == ai_id).first()
    rags = db.query(models.RAGTable).filter(models.RAGTable.ai_id == ai_id).all()
    chat_count = db.query(models.ChatMessageTable).filter(models.ChatMessageTable.sender_id == ai_id).count()
    like = is_ai_liked_by_user(db=db, user_address=user_address, ai_id=ai_id)
    daily_user_access = db.query(models.ChatTable).filter(models.ChatTable.ai_id == ai_id, models.ChatTable.daily_user_access == True).count()
    creator = db.query(models.UserTable).filter(models.UserTable.user_address == ai_table.creator_address).first().nickname

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
        chat_count=chat_count,
        creator = creator,
        total_prompt_token_usage=total_prompt_token_usage,
        total_completion_token_usage=total_completion_token_usage,
        total_token_usage=total_token_usage,
        daily_user_access=daily_user_access,  # Replace with actual logic if needed
        like=like
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
        ai_read = get_ai_by_id(db=db, ai_id=ai.id, user_address=user_address)
        my_ai_list.append(ai_read)

    return ai_schemas.AIReadList(ais=my_ai_list)

def get_today_ais(db: Session, user_address:str) -> ai_schemas.AIReadList:
    ais = db.query(models.AITable).order_by(models.AITable.created_at.desc()).limit(4).all()

    ai_list = []  # 결과를 담을 리스트
    for ai in ais:
        ai_read = get_ai_by_id(db=db, ai_id=ai.id, user_address=user_address)
        ai_list.append(ai_read)

    return ai_schemas.AIReadList(ais=ai_list) 

def search_ai_by_name(db: Session, name: str, user_address : str) -> ai_schemas.AIReadList:
    ais = db.query(models.AITable).filter(models.AITable.name.like(f"%{name}%")).all()

    ai_list = []  # 결과를 담을 리스트
    for ai in ais:
        ai_read = get_ai_by_id(db=db, ai_id=ai.id, user_address=user_address)
        ai_list.append(ai_read)

    # 최종 결과로 AIOVerviewList 반환
    return ai_schemas.AIReadList(ais=ai_list)

def get_category_trend_users(db: Session, offset: int, limit : int, category:str, user_address):
    query = db.query(models.AITable)

    # 카테고리가 "all"이 아닌 경우에만 필터 추가
    if category != "all":
        query = query.filter(models.AITable.category == category)

    # 페이지네이션 적용
    ais = query.offset(offset).limit(limit - offset).all()

    ai_list = []  # 결과를 담을 리스트
    for ai in ais:
        ai_read = get_ai_by_id(db=db, ai_id=ai.id, user_address=user_address)
        ai_list.append(ai_read)

    # 최종 결과로 AIOVerviewList 반환
    return ai_schemas.AIReadList(ais=ai_list) 

def get_ais_user_like(db: Session, user_address: str) -> ai_schemas.AIReadList:
    results = db.query(models.LikeTable, models.AITable) \
        .join(models.AITable, models.AITable.id == models.LikeTable.ai_id) \
        .filter(models.LikeTable.user_address == user_address).all()
    
    ais = []
    for like, ai in results:
        ai_read = get_ai_by_id(db=db, ai_id=ai.id, user_address=user_address)
        ais.append(ai_read)
    return ai_schemas.AIReadList(ais=ais)

def update_ai(db: Session, ai_update: ai_schemas.AIUpdate) -> ai_schemas.AIRead:
    db.query(models.AITable).filter(models.AITable.id == ai_update.id).update({
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
