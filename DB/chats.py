from sqlalchemy.orm import Session
from . import models, schemas
from .users import get_user

# # ChatTable CRUD functions
def get_chat(db: Session, chat_id: str):
    return db.query(models.ChatTable).filter(models.ChatTable.chat_id == chat_id).first()

def check_chat_by_ai_id(db: Session, ai_id: str):
    res = db.query(models.ChatTable).filter(models.ChatTable.ai_id == ai_id).all()
    if res:
        return True
    else:
        return False
    
def get_chats_by_user_address(db: Session, user_address: str):
    # Join AITable and ChatTable, filter by user_address
    results = (
        db.query(models.ChatTable, models.AITable)
        .join(models.AITable, models.ChatTable.ai_id == models.AITable.ai_id)
        .filter(models.ChatTable.user_address == user_address)
        .all()
    )

    # Use a list comprehension to build the chat overview list
    chats = [
        schemas.ChatTableOverView(
            chat_id=chat_info.chat_id,
            ai_id=chat_info.ai_id,
            category=ai_info.category,
            creator_address=ai_info.creator_address,
            image_url=ai_info.image_url,
            ai_name=ai_info.ai_name,
            creator=get_user(db=db, user_address=ai_info.creator_address).nickname,  # Retrieve creator's nickname
        )
        for chat_info, ai_info in results
    ]

    return schemas.ChatTableOverViewList(chats=chats)


def get_chats_by_ai_id(db: Session, ai_id: str):
    # Perform the join query and extract the necessary fields
    results = (
        db.query(models.ChatTable, models.AITable)
        .join(models.AITable, models.ChatTable.ai_id == models.AITable.ai_id)  # Explicit join condition
        .filter(models.ChatTable.ai_id == ai_id)
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


def create_chat(db: Session, chat: schemas.ChatRoom):
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


def check_chat_exists(db: Session, chat_id: str):
    res = db.query(models.ChatTable).filter(models.ChatTable.chat_id == chat_id).first()
    if res:
        return True
    else:
        return False

# # ChatContentsTable CRUD functions
def get_chat_contents(db: Session, chat_id: str):
    check_chat = check_chat_exists(db=db, chat_id=chat_id)  # 여기서 'chat_id=str' 대신 'chat_id=chat_id'
    if check_chat:
        chat_info = get_chat(db=db, chat_id=chat_id)
        if not chat_info.daily_user_access:
            chat_info.daily_user_access = True
            db.commit()  # 변경 사항을 DB에 반영
            db.refresh(chat_info)
        res = db.query(models.ChatContentsTable).filter(models.ChatContentsTable.chat_id == chat_id).all()
    else:
        res = []
    return schemas.ChatContentsTableListOut(chats=res)


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