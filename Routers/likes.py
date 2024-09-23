from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from DB import chats, utils, users, ais, likes
from Schema import base_schemas, like_schemas, ai_schemas

router = APIRouter()


# Create a like for an AI by a user
@router.post("/", response_model=like_schemas.LikeCreate)
def create_like(like_create: like_schemas.LikeCreate, db: Session = Depends(utils.get_db)):
    # Check if the user has already liked the AI
    already_liked = likes.is_ai_liked_by_user(db, user_address=like_create.user_address, ai_id=like_create.ai_id)
    if already_liked:
        raise HTTPException(status_code=400, detail="AI already liked by this user")

    db_like = likes.create_user_like_ai(db, user_address=like_create.user_address, ai_id=like_create.ai_id)
    return db_like

# Delete a like for an AI by a user
@router.delete("/", response_model=bool)
def delete_like(like_create: like_schemas.LikeCreate, db: Session = Depends(utils.get_db)):
    success = likes.delete_user_like_ai(db, user_address=like_create.user_address, ai_id=like_create.ai_id)
    if not success:
        raise HTTPException(status_code=404, detail="Like not found or already deleted")
    return success