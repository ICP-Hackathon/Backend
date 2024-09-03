from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from DB import crud, models, schemas
from DB.database import SessionLocal, engine

from AI.crud import add_text

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
@app.post("/user/", response_model=schemas.UserTableOut)
def create_user(user: schemas.UserTableCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, userid=user.userid)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)

# 특정 사용자 읽기
@app.get("/user/{userid}", response_model=schemas.UserTableOut)
def read_user(userid: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, userid=userid)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 사용자 정보 업데이트
@app.put("/user/{userid}", response_model=schemas.UserTableOut)
def update_user(userid: str, user_update: schemas.UserTableUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db=db, userid=userid, user_update=user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# 사용자 삭제
# @app.delete("/user/{userid}", response_model=schemas.UserTableOut)
# def delete_user(userid: str, db: Session = Depends(get_db)):
#     deleted_user = crud.delete_user(db=db, userid=userid)
#     if not deleted_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return deleted_user

# AI 생성
@app.post("/ai/", response_model=schemas.AITableOut)
def create_ai(ai: schemas.AITableCreate, db: Session = Depends(get_db)):
    # AI 콘텐츠를 추가하는 로직
    add_text([ai.contents], [{"source" : ""}], [ai.name + "tx"])

    aiDB = schemas.AITableBase(
        id=ai.id,  # AI 객체의 고유 식별자
        name=ai.name,  # 이름 필드, None이 기본값
        category=ai.category,  # 카테고리 필드, None이 기본값
        introductions=ai.introductions  # 소개 필드, None이 기본값
    )

# AI 테이블에 새로운 항목 생성
    created_ai = crud.create_ai(db=db, ai=aiDB)
    
    # AILog 테이블에 로그 기록
    ailog = schemas.AILogTableCreate(
        aiid=ai.id,
        log=ai.logs,
        txurl="create",
    )
    crud.create_ailog(db=db, ailog=ailog)
    
    return created_ai

@app.get("/ai/top10/", response_model=schemas.AITableListOut)
def read_top_10_ais(db: Session = Depends(get_db)):
    ais = db.query(models.AITable).order_by(models.AITable.usage.desc()).limit(10).all()
    return schemas.AITableListOut(ais=ais)

# 특정 AI 읽기
@app.get("/ai/{ai_id}", response_model=schemas.AITableOut)
def read_ai(ai_id: str, db: Session = Depends(get_db)):
    db_ai = crud.get_ai(db, ai_id=ai_id)
    if not db_ai:
        raise HTTPException(status_code=404, detail="AI not found")
    return db_ai

# AI 정보 업데이트
@app.put("/ai/{ai_id}", response_model=schemas.AITableOut)
def update_ai(ai_id: str, ai_update: schemas.AITableUserUpdate, db: Session = Depends(get_db)):
    # AI 콘텐츠가 변경된 경우 add_text 호출
    if ai_update.contents != "":
        add_text([ai_update.contents], [{"source" : ai_update.name}], [ai_update.name + "UPDATE"])
    
    aiUpdateDB = schemas.AITableBase(
        id=ai_id,  # AI 객체의 고유 식별자
        name=ai_update.name,  # 이름 필드, None이 기본값
        category=ai_update.category,  # 카테고리 필드, None이 기본값
        introductions=ai_update.introductions  # 소개 필드, None이 기본값
    )

    # AI 정보를 업데이트
    updated_ai = crud.update_ai(db=db, ai_id=ai_id, ai_update=aiUpdateDB)
    if not updated_ai:
        raise HTTPException(status_code=404, detail="AI not found")
    
    # AILog 테이블에 로그 기록
    ailog = schemas.AILogTableCreate(
        aiid=ai_id,
        log=ai_update.logs,
        txurl="create",
    )

    crud.create_ailog(db=db, ailog=ailog)
    
    return updated_ai

# AI 삭제
@app.delete("/ai/{ai_id}", response_model=schemas.AITableOut)
def delete_ai(ai_id: str, db: Session = Depends(get_db)):
    deleted_ai = crud.delete_ai(db=db, ai_id=ai_id)
    if not deleted_ai:
        raise HTTPException(status_code=404, detail="AI not found")
    return deleted_ai

# 특정 AI의 특정 로그 읽기
@app.get("/ailogs/{log_id}", response_model=schemas.AILogTableOut)
def read_ailog(log_id: str, db: Session = Depends(get_db)):
    db_ailog = crud.get_ailog(db, log_id=log_id)
    if not db_ailog:
        raise HTTPException(status_code=404, detail="Log not found")
    return db_ailog

#특정 AI 로그 목록 보기
@app.get("/ailogs/ai/{ai_id}", response_model=schemas.AILogTableListOut)
def read_ailog_by_aiid(ai_id: str, db: Session = Depends(get_db)):
    db_ailogs = crud.get_ailogs_by_aiid(db, ai_id=ai_id)
    if not db_ailogs:
        raise HTTPException(status_code=404, detail="Log not found")
    return schemas.AILogTableListOut(logs=db_ailogs)

# AI 로그 정보 업데이트
# @app.put("/ailogs/{log_id}", response_model=schemas.AILogTableOut)
# def update_ailog(log_id: str, ailog_update: schemas.AILogTableUpdate, db: Session = Depends(get_db)):
#     updated_ailog = crud.update_ailog(db=db, log_id=log_id, ailog_update=ailog_update)
#     if not updated_ailog:
#         raise HTTPException(status_code=404, detail="Log not found")
#     return updated_ailog

# AI 로그 삭제
# @app.delete("/ailogs/{log_id}", response_model=schemas.AILogTableOut)
# def delete_ailog(log_id: str, db: Session = Depends(get_db)):
#     deleted_ailog = crud.delete_ailog(db=db, log_id=log_id)
#     if not deleted_ailog:
#         raise HTTPException(status_code=404, detail="Log not found")
#     return deleted_ailog

# 채팅 생성
@app.post("/chats/", response_model=schemas.ChatTableOut)
def create_chat(chat: schemas.ChatTableCreate, db: Session = Depends(get_db)):
    return crud.create_chat(db=db, chat=chat)

# 유저 채팅 목록 읽기
@app.get("/chats/{userid}", response_model=schemas.ChatTableOut)
def read_chat(userid: str, db: Session = Depends(get_db)):
    db_chat = crud.get_chat(db, user_id=userid)
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return db_chat

# 채팅 정보 업데이트
# @app.put("/chats/{chat_id}", response_model=schemas.ChatTableOut)
# def update_chat(chat_id: str, chat_update: schemas.ChatTableUpdate, db: Session = Depends(get_db)):
#     updated_chat = crud.update_chat(db=db, chat_id=chat_id, chat_update=chat_update)
#     if not updated_chat:
#         raise HTTPException(status_code=404, detail="Chat not found")
#     return updated_chat

# 채팅 삭제
@app.delete("/chats/{chat_id}", response_model=schemas.ChatTableOut)
def delete_chat(chat_id: str, db: Session = Depends(get_db)):
    deleted_chat = crud.delete_chat(db=db, chat_id=chat_id)
    if not deleted_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return deleted_chat

# 채팅 내용 생성
@app.post("/chatcontent/", response_model=schemas.ChatContentsTableOut)
def create_chat_content(chat_content: schemas.ChatContentsTableCreate, db: Session = Depends(get_db)):
    return crud.create_chat_content(db=db, chat_content=chat_content)

# 특정 채팅 내용 읽기
@app.get("/chatcontents/{chat_id}", response_model=schemas.ChatContentsTableOut)
def read_chat_content(chat_id: str, db: Session = Depends(get_db)):
    db_chat_content = crud.get_chat_contents(db, chat_id=chat_id)
    if not db_chat_content:
        raise HTTPException(status_code=404, detail="Chat content not found")
    return schemas.ChatContentsTableOut(chats=db_chat_content)

# 채팅 내용 업데이트
# @app.put("/chatcontents/{chatcontentsid}", response_model=schemas.ChatContentsTableOut)
# def update_chat_content(chatcontentsid: str, chat_content_update: schemas.ChatContentsTableUpdate, db: Session = Depends(get_db)):
#     updated_chat_content = crud.update_chat_content(db=db, chat_content_id=chatcontentsid, chat_content_update=chat_content_update)
#     if not updated_chat_content:
#         raise HTTPException(status_code=404, detail="Chat content not found")
#     return updated_chat_content

# 채팅 내용 삭제
# @app.delete("/chatcontents/{chatcontentsid}", response_model=schemas.ChatContentsTableOut)
# def delete_chat_content(chatcontentsid: str, db: Session = Depends(get_db)):
#     deleted_chat_content = crud.delete_chat_content(db=db, chat_content_id=chatcontentsid)
#     if not deleted_chat_content:
#         raise HTTPException(status_code=404, detail="Chat content not found")
#     return deleted_chat_content