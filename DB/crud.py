from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

#################### UserTable CRUD functions ###################

def get_users(db: Session, offset: int, limit: int):
    return db.query(models.UserTable).offset(offset).limit(limit - offset).all()

def get_user(db: Session, user_address: str):
    return db.query(models.UserTable).filter(models.UserTable.user_address == user_address).first()

def check_user_exists(db: Session, user_address: str):
    res =  db.query(models.UserTable).filter(models.UserTable.user_address == user_address).first()
    if res:
        return True
    else:
        return False

def add_user(db: Session, user: schemas.UserTableBase):
    db_user = models.UserTable(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# def update_user(db: Session, userid: str, user_update: schemas.UserTableBase):
#     db_user = get_user(db, userid)
#     if db_user:
#         for key, value in user_update.model_dump(exclude_unset=True).items():
#             setattr(db_user, key, value)
#         db.commit()
#         db.refresh(db_user)
#     return db_user

# def delete_user(db: Session, userid: str):
#     db_user = get_user(db, userid)
#     if db_user:
#         db.delete(db_user)
#         db.commit()
#     return db_user

################### AITable CRUD functions ###################

def get_ais(db: Session, offset: int, limit: int):
    return db.query(models.AITable).offset(offset).limit(limit-offset).all()

def get_ai(db: Session, ai_id: str):
    return db.query(models.AITable).filter(models.AITable.ai_id == ai_id).first()

def get_user_ais(db: Session, user_address : str):
    return db.query(models.AITable).filter(models.AITable.creator_address == user_address).all()

def get_rags(db: Session, ai_id: str):
    return db.query(models.RAGTable).filter(models.AITable.ai_id == ai_id).all()

def get_ai_detail(db: Session, ai_id: str) -> schemas.AIDetail:
    # AITable과 RAGTable을 ai_id로 조인
    result = (
        db.query(models.AITable, models.RAGTable)
        .join(models.RAGTable, models.AITable.ai_id == models.RAGTable.ai_id)
        .filter(models.AITable.ai_id == ai_id)
        .all()
    )
    
    if not result:
        return None  # 해당 ai_id에 대한 데이터가 없는 경우 처리
    
    # AITable 정보는 첫 번째 레코드에서 가져옵니다
    ai, _ = result[0]

    # RAGTable 데이터는 모든 레코드에서 logs로 변환합니다
    logs = [schemas.RAGTableBase.model_validate(rag) for _, rag in result]

    # AIDetail 스키마로 반환
    ai_detail = schemas.AIDetail(
        ai_id=ai.ai_id,
        creator_address=ai.creator_address,
        created_at=ai.created_at,
        name=ai.name,
        image_url=ai.image_url,
        category=ai.category,
        introductions=ai.introductions,
        chat_counts=ai.chat_counts,
        prompt_tokens=ai.prompt_tokens,
        completion_tokens=ai.completion_tokens,
        weekly_users=ai.weekly_users,
        logs=logs  # logs는 RAGTableBase 리스트로 설정
    )
    
    return ai_detail


def get_ais_by_weekly_users(db: Session, offset: int, limit : int):
    return db.query(models.AITable).order_by(models.AITable.weekly_users.desc()).offset(offset).limit(limit - offset).all()

def get_today_ais(db: Session):
    # Join the tables and fetch the data
    results = db.query(models.AITable, models.UserTable)\
        .join(models.UserTable, models.AITable.creator_address == models.UserTable.user_address)\
        .order_by(models.AITable.created_at.desc())\
        .limit(4).all()

    ais = []
    # Manually map each result to the AITableOut schema
    for ait, user in results:
        ai_out = schemas.AITableOut(
            ai_id=ait.ai_id,
            creator_address=ait.creator_address,
            created_at=ait.created_at,
            name=ait.name,
            image_url=ait.image_url,
            category=ait.category,
            introductions=ait.introductions,
            chat_counts=ait.chat_counts,
            prompt_tokens=ait.prompt_tokens,
            completion_tokens=ait.completion_tokens,
            weekly_users=ait.weekly_users,
            creator=user.nickname  # Mapping the nickname to the `creator` field
        )
        ais.append(ai_out)
    
    return ais

def get_category_ais_by_weekly_users(db: Session, offset: int, limit : int, category:str):
    return db.query(models.AITable).filter(models.AITable.category == category).order_by(models.AITable.weekly_users.desc()).offset(offset).limit(limit - offset).all()

def search_ai(db: Session, name: str):
    return db.query(models.AITable).filter(models.AITable.name.like(f"%{name}%")).all()

# # AITable CRUD functions
# def get_top_10_ai_by_usage(db: Session):
#     return db.query(models.AITable).order_by(models.AITable.usage.desc()).limit(10).all()

def create_ai(db: Session, ai: schemas.AITableCreate):
    db_ai = models.AITable(**ai.model_dump())
    db.add(db_ai)
    db.commit()
    db.refresh(db_ai)
    return db_ai

def update_ai(db: Session, ai_id: str, ai_update: schemas.AITableUserUpdateInput):
    aiUpdateDB = schemas.AITableUpdate(
        name = ai_update.name,
        image_url = ai_update.image_url,
        category= ai_update.category,  # 카테고리 필드, None이 기본값
        introductions=ai_update.introductions  # 소개 필드, None이 기본값
    )
    
    db_ai = get_ai(db, ai_id)
    if db_ai:
        for key, value in aiUpdateDB.model_dump(exclude_unset=True).items():
            setattr(db_ai, key, value)
        db.commit()
        db.refresh(db_ai)
    return db_ai

def update_usage_ai(db: Session, ai_id: str, ai_update: schemas.AITableUsageUpdate):
    db_ai = get_ai(db, ai_id)
    if db_ai:
        for key, value in ai_update.model_dump(exclude_unset=True).items():
            setattr(db_ai, key, value)
        db.commit()
        db.refresh(db_ai)
    return db_ai

# def update_collect_ai(db: Session, aiid: str, ai_update: schemas.AITableCollectUpdate):
#     db_ai = get_ai(db, aiid)
#     if db_ai:
#         for key, value in ai_update.model_dump(exclude_unset=True).items():
#             setattr(db_ai, key, value)
#         db.commit()
#         db.refresh(db_ai)
#     return db_ai

def delete_ai(db: Session, ai_id: str):
    db_ai = get_ai(db, ai_id)
    if db_ai:
        db.delete(db_ai)
        db.commit()
    return db_ai

# # AILogTable CRUD functions
# def get_ailog(db: Session, log_id: str):
#     return db.query(models.AILogTable).filter(models.AILogTable.id == log_id).first()

# # RAGTable CRUD functions
def get_raglogs_by_aiid(db: Session, ai_id: str):
    return db.query(models.RAGTable).filter(models.RAGTable.ai_id == ai_id).all()

def create_rag(db: Session, ai_update: schemas.AITableUserUpdateInput, digest: str, faiss_id: str):
    rag = schemas.RAGTableCreate(
        ai_id = ai_update.ai_id,
        created_at = datetime.now(),
        comments =ai_update.comments,
        tx_url= digest,
        faissid = faiss_id
    )
    db_rag = models.RAGTable(**rag.model_dump())
    db.add(db_rag)
    db.commit()
    db.refresh(db_rag)
    return db_rag

# def update_ailog(db: Session, log_id: str, ailog_update: schemas.AILogTableCreate):
#     db_ailog = get_ailog(db, log_id)
#     if db_ailog:
#         for key, value in ailog_update.model_dump(exclude_unset=True).items():
#             setattr(db_ailog, key, value)
#         db.commit()
#         db.refresh(db_ailog)
#     return db_ailog

# def delete_ailog(db: Session, log_id: str):
#     db_ailog = get_ailog(db, log_id)
#     if db_ailog:
#         db.delete(db_ailog)
#         db.commit()
#     return db_ailog

def delete_raglogs(db: Session, ai_id: str):
    # AI ID와 관련된 모든 로그를 가져옴
    ailogs = get_raglogs_by_aiid(db, ai_id)

    if not ailogs:
        return None  # 로그가 없으면 None 반환

    # 각 로그를 순회하며 삭제
    for log in ailogs:
        db.delete(log)

    # 모든 로그를 삭제한 후 commit
    db.commit()

    return ailogs  # 삭제된 로그 목록 반환
# # ChatTable CRUD functions
def get_chat(db: Session, chat_id: str):
    return db.query(models.ChatTable).filter(models.ChatTable.chat_id == chat_id).first()

def get_chats(db: Session, user_address: str):
    # Perform the join query and extract the necessary fields
    results = (
        db.query(models.ChatTable, models.AITable)
        .join(models.AITable, models.ChatTable.ai_id == models.AITable.ai_id)  # Explicit join condition
        .filter(models.ChatTable.user_address == user_address)
        .all()
    )
    
    # Combine the data into a single response format
    chats = []
    for chat, ai in results:
        chat_data = {
            'chat_id': chat.chat_id,
            'ai_id': chat.ai_id,
            'user_address': chat.user_address,
            'name': ai.name,
            'category': ai.category,
            'creator_address': ai.creator_address,
            'created_at': ai.created_at,
            'image_url': ai.image_url,
            'introductions': ai.introductions,
            'chat_counts': ai.chat_counts,
            'prompt_tokens': ai.prompt_tokens,
            'completion_tokens': ai.completion_tokens,
            'weekly_users': ai.weekly_users,
        }
        chats.append(chat_data)
    
    return chats


def create_chat(db: Session, chat: schemas.ChatTableBase):
    db_chat = models.ChatTable(**chat.model_dump())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

# # def update_chat(db: Session, chat_id: str, chat_update: schemas.ChatTableUpdate):
# #     db_chat = get_chat(db, chat_id)
# #     if db_chat:
# #         for key, value in chat_update.model_dump(exclude_unset=True).items():
# #             setattr(db_chat, key, value)
# #         db.commit()
# #         db.refresh(db_chat)
# #     return db_chat

# def delete_chat(db: Session, chat_id: str):
#     db_chat = get_chat(db, chat_id)
#     if db_chat:
#         db.delete(db_chat)
#         db.commit()
#     return db_chat

# # ChatContentsTable CRUD functions
def get_chat_contents(db: Session, chat_id: str):
    return db.query(models.ChatContentsTable).filter(models.ChatContentsTable.chat_id == chat_id).all()


def create_chat_content(db: Session, chat_content: schemas.ChatContentsTableCreate):
    db_chat_content = models.ChatContentsTable(**chat_content.model_dump())
    db.add(db_chat_content)
    db.commit()
    db.refresh(db_chat_content)
    return db_chat_content

# # def update_chat_content(db: Session, chat_content_id: str, chat_content_update: schemas.ChatContentsTableUpdate):
# #     db_chat_content = get_chat_content(db, chat_content_id)
# #     if db_chat_content:
# #         for key, value in chat_content_update.model_dump(exclude_unset=True).items():
# #             setattr(db_chat_content, key, value)
# #         db.commit()
# #         db.refresh(db_chat_content)
# #     return db_chat_content

# # def delete_chat_content(db: Session, chat_content_id: str):
# #     db_chat_content = get_chat_content(db, chat_content_id)
# #     if db_chat_content:
# #         db.delete(db_chat_content)
# #         db.commit()
# #     return db_chat_content