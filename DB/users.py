from typing import List
from sqlalchemy.orm import Session

from DB import models
from Schema import base_schemas

def get_users(db: Session, offset: int, limit: int) -> List[models.UserTable]:
    return db.query(models.UserTable).offset(offset).limit(limit - offset).all()

def get_user(db: Session, user_address: str) -> models.UserTable:
    return db.query(models.UserTable).filter(models.UserTable.user_address == user_address).first()

def check_user_exists(db: Session, user_address: str) -> bool:
    return db.query(models.UserTable).filter(models.UserTable.user_address == user_address).first() is not None

def add_user(db: Session, user: base_schemas.User) -> models.UserTable:
    db_user = models.UserTable(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_update: base_schemas.User) -> models.UserTable:
    db_user = get_user(db, user_update.user_address)
    if db_user:
        for key, value in user_update.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

# def delete_user(db: Session, userid: str):
#     db_user = get_user(db, userid)
#     if db_user:
#         db.delete(db_user)
#         db.commit()
#     return db_user
