from sqlalchemy.orm import Session
from . import models, schemas

################### LikeTable CRUD functions ###################

def get_user_like_ais(db: Session, user_address: str):
    results = db.query(models.LikeTable, models.AITable) \
        .join(models.AITable, models.AITable.ai_id == models.LikeTable.ai_id) \
        .filter(models.LikeTable.user_address == user_address).all()
    
    liked_ais = []
    for like, ai in results:
        liked_ai = schemas.LikedAIOut(
            like_id=like.like_id,
            user_address=like.user_address,
            ai_id=ai.ai_id,
            creator_address=ai.creator_address,
            ai_name=ai.ai_name,
            image_url=ai.image_url,
            category=ai.category,
        )
        liked_ais.append(liked_ai)
    return liked_ais

def check_like(db: Session, user_address: str, ai_id: str) -> bool:
    return db.query(models.LikeTable).filter(
        models.LikeTable.user_address == user_address,
        models.LikeTable.ai_id == ai_id
    ).first() is not None

def is_ai_liked_by_user(db: Session, user_address: str, ai_id: str) -> bool:

    return db.query(models.LikeTable).filter(
        models.LikeTable.user_address == user_address,
        models.LikeTable.ai_id == ai_id
    ).first() is not None

def create_user_like_ai(db: Session, user_address: str, ai_id: str):
    db_like = models.LikeTable(user_address=user_address, ai_id=ai_id)
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


def delete_user(db: Session, user_address: str):
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
