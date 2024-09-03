from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from DB import crud, models, schemas
from DB.database import SessionLocal, engine

# 데이터베이스 테이블 생성하기
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 종속성 만들기: 요청 당 독립적인 데이터베이스 세션/연결이 필요하고 요청이 완료되면 닫음
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# 사용자 생성
@app.post("/profiles/", response_model=schemas.Profile)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=profile.user_name)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=profile)

# 모든 사용자 읽기
@app.get("/profiles/", response_model=List[schemas.Profile])
def read_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    profiles = crud.get_users(db, skip=skip, limit=limit)
    return profiles

# 특정 사용자 읽기
@app.get("/profiles/{user_name}", response_model=schemas.Profile)
def read_profile(user_name: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_name)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 사용자 정보 업데이트
@app.put("/profiles/{user_name}", response_model=schemas.Profile)
def update_profile(user_name: str, profile_update: schemas.ProfileCreate, db: Session = Depends(get_db)):
    updated_user = crud.update_profile(db=db, user_name=user_name, updated_data=profile_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# 다이어리 생성
@app.post("/diaries/{user_name}", response_model=schemas.DiaryCreate)
def create_diary_for_user(
    user_name: str, diary: schemas.DiaryCreate, db: Session = Depends(get_db)
):
    db_user = crud.get_user(db, user_id=user_name)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_diary = models.DiaryModel(**diary.model_dump())
    db.add(db_diary)
    db.commit()
    db.refresh(db_diary)
    return db_diary


@app.get("/diaries/{user_name}", response_model=List[schemas.DiaryRead])
def read_diaries(skip: int = 0, limit: int = 100, user_name: str = None, db: Session = Depends(get_db)):
    diaries = crud.get_diaries(db, user_id=user_name, skip=skip, limit=limit)
    return diaries