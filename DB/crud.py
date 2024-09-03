from sqlalchemy.orm import Session
from . import models, schemas

# UserTable CRUD functions
def get_user(db: Session, userid: str):
    return db.query(models.UserTable).filter(models.UserTable.userid == userid).first()

def create_user(db: Session, user: schemas.UserTableCreate):
    db_user = models.UserTable(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, userid: str, user_update: schemas.UserTableUpdate):
    db_user = get_user(db, userid)
    if db_user:
        for key, value in user_update.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, userid: str):
    db_user = get_user(db, userid)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# AITable CRUD functions
def get_ai(db: Session, ai_id: str):
    return db.query(models.AITable).filter(models.AITable.id == ai_id).first()

def create_ai(db: Session, ai: schemas.AITableCreate):
    db_ai = models.AITable(**ai.model_dump())
    db.add(db_ai)
    db.commit()
    db.refresh(db_ai)
    return db_ai

def update_ai(db: Session, ai_id: str, ai_update: schemas.AITableUserUpdate):
    db_ai = get_ai(db, ai_id)
    if db_ai:
        for key, value in ai_update.model_dump(exclude_unset=True).items():
            setattr(db_ai, key, value)
        db.commit()
        db.refresh(db_ai)
    return db_ai

def delete_ai(db: Session, ai_id: str):
    db_ai = get_ai(db, ai_id)
    if db_ai:
        db.delete(db_ai)
        db.commit()
    return db_ai

# AILogTable CRUD functions
def get_ailog(db: Session, log_id: str):
    return db.query(models.AILogTable).filter(models.AILogTable.id == log_id).first()

# AILogTable CRUD functions
def get_ailogs_by_aiid(db: Session, ai_id: str):
    return db.query(models.AILogTable).filter(models.AILogTable.aiid == ai_id).all()

def create_ailog(db: Session, ailog: schemas.AILogTableCreate):
    db_ailog = models.AILogTable(**ailog.model_dump())
    db.add(db_ailog)
    db.commit()
    db.refresh(db_ailog)
    return db_ailog

def update_ailog(db: Session, log_id: str, ailog_update: schemas.AILogTableUpdate):
    db_ailog = get_ailog(db, log_id)
    if db_ailog:
        for key, value in ailog_update.model_dump(exclude_unset=True).items():
            setattr(db_ailog, key, value)
        db.commit()
        db.refresh(db_ailog)
    return db_ailog

def delete_ailog(db: Session, log_id: str):
    db_ailog = get_ailog(db, log_id)
    if db_ailog:
        db.delete(db_ailog)
        db.commit()
    return db_ailog

# ChatTable CRUD functions
def get_chat(db: Session, chat_id: str):
    return db.query(models.ChatTable).filter(models.ChatTable.chatid == chat_id).first()

def create_chat(db: Session, chat: schemas.ChatTableCreate):
    db_chat = models.ChatTable(**chat.model_dump())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def update_chat(db: Session, chat_id: str, chat_update: schemas.ChatTableUpdate):
    db_chat = get_chat(db, chat_id)
    if db_chat:
        for key, value in chat_update.model_dump(exclude_unset=True).items():
            setattr(db_chat, key, value)
        db.commit()
        db.refresh(db_chat)
    return db_chat

def delete_chat(db: Session, chat_id: str):
    db_chat = get_chat(db, chat_id)
    if db_chat:
        db.delete(db_chat)
        db.commit()
    return db_chat

# ChatContentsTable CRUD functions
def get_chat_contents(db: Session, chat_id: str):
    return db.query(models.ChatContentsTable).filter(models.ChatContentsTable.chatid == chat_id).all()


def create_chat_content(db: Session, chat_content: schemas.ChatContentsTableCreate):
    db_chat_content = models.ChatContentsTable(**chat_content.model_dump())
    db.add(db_chat_content)
    db.commit()
    db.refresh(db_chat_content)
    return db_chat_content

# def update_chat_content(db: Session, chat_content_id: str, chat_content_update: schemas.ChatContentsTableUpdate):
#     db_chat_content = get_chat_content(db, chat_content_id)
#     if db_chat_content:
#         for key, value in chat_content_update.model_dump(exclude_unset=True).items():
#             setattr(db_chat_content, key, value)
#         db.commit()
#         db.refresh(db_chat_content)
#     return db_chat_content

# def delete_chat_content(db: Session, chat_content_id: str):
#     db_chat_content = get_chat_content(db, chat_content_id)
#     if db_chat_content:
#         db.delete(db_chat_content)
#         db.commit()
#     return db_chat_content
