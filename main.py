from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from DB import crud, models, schemas
from DB.database import SessionLocal, engine

from AI.crud import add_text, delete_text
from AI.main import rag_qa
from fastapi.middleware.cors import CORSMiddleware



import random
from time import ctime


# 데이터베이스 테이블 생성하기
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 허용할 클라이언트의 도메인
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메서드 (GET, POST, OPTIONS 등)
    allow_headers=["*"],  # 허용할 헤더
)



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

# 유저가 지갑 연결
@app.post("/login/", response_model=schemas.UserTableBase)
def login_or_create_user(user: schemas.UserTableCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, userid=user.userid)
    if db_user:
        return db_user  # 사용자가 이미 존재하면 사용자 정보 반환
    else:
        # 사용자가 존재하지 않으면 새로 생성
        return crud.create_user(db=db, user=user)

# 사용자 정보 업데이트
@app.put("/user/{userid}", response_model=schemas.UserTableBase)
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
@app.post("/ai/", response_model=schemas.AITableBase)
def create_ai(ai: schemas.AITableCreate, db: Session = Depends(get_db)):
    aiid = ai.creator + '_' + ai.name

    faiss_id = ai.name + "tx" + str(random.random())
    # AI 콘텐츠를 추가하는 로직
    embed = add_text([ai.contents], [{"source" : aiid}], [faiss_id])

    #먼저 만들어졌었는지 확인
    db_ai = crud.get_ai(db, aiid=aiid)
    if db_ai:
        raise HTTPException(status_code=400, detail="AI with this ID already exists")
    
    aiDB = schemas.AITableBase(
        id=aiid,  # AI 객체의 고유 식별자
        creator=ai.creator, #만든사람
        name=ai.name,  # 이름 필드, None이 기본값
        category=ai.category,  # 카테고리 필드, None이 기본값
        introductions=ai.introductions  # 소개 필드, None이 기본값
    )

    # AI 테이블에 새로운 항목 생성
    created_ai = crud.create_ai(db=db, ai=aiDB)
    
    # AILog 테이블에 로그 기록
    ailog = schemas.AILogTableCreate(
        aiid=aiid,
        log=ai.logs,
        txurl="create",
        faissid = faiss_id
    )
    crud.create_ailog(db=db, ailog=ailog)
    
    return created_ai
#인기있는 AI 보기
@app.get("/ai/top10/", response_model=schemas.AITableListOut)
def read_top_10_ais(db: Session = Depends(get_db)):
    ais = db.query(models.AITable).order_by(models.AITable.usage.desc()).limit(10).all()
    return schemas.AITableListOut(ais=ais)

# 내 AI 보기
@app.get("/ai/myais/{userid}", response_model=schemas.AITableListOut)
def read_my_ais(userid : str, db: Session = Depends(get_db)):
    ais = db.query(models.AITable).filter(models.AITable.creator == userid).all()
    return schemas.AITableListOut(ais=ais)

# 특정 AI 읽기
@app.get("/ai/{aiid}", response_model=schemas.AITableBase)
def read_ai(aiid: str, db: Session = Depends(get_db)):
    db_ai = crud.get_ai(db, aiid=aiid)
    if not db_ai:
        raise HTTPException(status_code=404, detail="AI not found")
    return db_ai

@app.get("/ai/search/{ainame}", response_model=schemas.AISearchListOut)
def search_ai(ainame: str, db: Session = Depends(get_db)):
    db_ai = crud.search_ai(db, name=ainame)
    if not db_ai:
        raise HTTPException(status_code=404, detail="AI not found")
    search_results = [
        schemas.AISearch(
            name=ai.name,
            creator=ai.creator,
            image=ai.image
        ) for ai in db_ai
    ]
    return schemas.AISearchListOut(ais=search_results)


# AI 정보 업데이트
@app.put("/ai/{aiid}", response_model=schemas.AITableBase)
def update_ai(aiid: str, ai_update: schemas.AITableUserUpdateInput, db: Session = Depends(get_db)):
    db_ai = crud.get_ai(db, aiid=aiid)
    if not db_ai:
        raise HTTPException(status_code=400, detail="AI Not found")

    faiss_id = None
    # AI 콘텐츠가 변경된 경우 add_text 호출
    if ai_update.contents != "":
        faiss_id = db_ai.name + "tx" + str(random.random())
        embed = add_text([ai_update.contents], [{"source" : db_ai.id}], [faiss_id])
        print(embed)
    
    aiUpdateDB = schemas.AITableUserUpdate(
        category=ai_update.category,  # 카테고리 필드, None이 기본값
        introductions=ai_update.introductions  # 소개 필드, None이 기본값
    )

    # AI 정보를 업데이트
    updated_ai = crud.update_ai(db=db, aiid=aiid, ai_update=aiUpdateDB)
    if not updated_ai:
        raise HTTPException(status_code=404, detail="AI not found")
    
    # AILog 테이블에 로그 기록
    ailog = schemas.AILogTableCreate(
        aiid=aiid,
        log=ai_update.logs,
        txurl="UPDATE",
        faissid = faiss_id
    )

    crud.create_ailog(db=db, ailog=ailog)
    
    return updated_ai

# AI 삭제
@app.delete("/ai/{aiid}", response_model=schemas.AITableBase)
def delete_ai(aiid: str, db: Session = Depends(get_db)):

    db_ai = crud.get_ai(db, aiid=aiid)
    if not db_ai:
        raise HTTPException(status_code=404, detail="AI not found")
    
    deleted_ai = crud.delete_ai(db=db, ai_id=aiid)

    ai_logs = crud.get_ailogs_by_aiid(db=db, aiid=aiid)
    ids = [i.faissid for i in ai_logs]
    delete_text(ids)

    crud.delete_ailogs(db=db, aiid=aiid)

    if not deleted_ai:
        raise HTTPException(status_code=404, detail="AI not found")
    return deleted_ai

# 특정 AI의 특정 로그 읽기
# @app.get("/ailogs/{log_id}", response_model=schemas.AILogTableOut)
# def read_ailog(log_id: str, db: Session = Depends(get_db)):
#     db_ailog = crud.get_ailog(db, log_id=log_id)
#     if not db_ailog:
#         raise HTTPException(status_code=404, detail="Log not found")
#     return db_ailog

#특정 AI 로그 목록 보기
@app.get("/ailogs/ai/{aiid}", response_model=schemas.AILogTableListOut)
def read_ailog_by_aiid(aiid: str, db: Session = Depends(get_db)):
    db_ailogs = crud.get_ailogs_by_aiid(db, aiid=aiid)
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
@app.post("/chats/", response_model=schemas.ChatTableBase)
def create_chat(chat: schemas.ChatTableCreate, db: Session = Depends(get_db)):
    db_ai = crud.get_ai(db, aiid=chat.aiid)
    if not db_ai:
        raise HTTPException(status_code=404, detail="AI not found")

    chatid = chat.userid + '_' + chat.aiid

    chat_exist = crud.get_chat(db, chatid=chatid)
    if chat_exist:
        raise HTTPException(status_code=400, detail="Chat already exists")

    chatTable = schemas.ChatTableBase(
        chatid=chatid,
        userid=chat.userid,
        aiid= chat.aiid,
    )

    return crud.create_chat(db=db, chat=chatTable)

# 유저 채팅 목록 읽기
@app.get("/chats/{userid}", response_model=schemas.ChatTableListOut)
def read_chat(userid: str, db: Session = Depends(get_db)):
    db_chat = crud.get_chats(db, userid=userid)
    return schemas.ChatTableListOut(chats=db_chat)

# 채팅 정보 업데이트
# @app.put("/chats/{chat_id}", response_model=schemas.ChatTableOut)
# def update_chat(chat_id: str, chat_update: schemas.ChatTableUpdate, db: Session = Depends(get_db)):
#     updated_chat = crud.update_chat(db=db, chat_id=chat_id, chat_update=chat_update)
#     if not updated_chat:
#         raise HTTPException(status_code=404, detail="Chat not found")
#     return updated_chat

# 채팅 삭제
@app.delete("/chats/{chat_id}", response_model=schemas.ChatTableBase)
def delete_chat(chat_id: str, db: Session = Depends(get_db)):
    deleted_chat = crud.delete_chat(db=db, chat_id=chat_id)
    if not deleted_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return deleted_chat

# 채팅 내용 생성
@app.post("/chatcontent/{chat_id}", response_model=schemas.ChatContentsTableBase)
def create_chat_content(chat_content: schemas.ChatContentsTableCreateInput, chat_id :str, db: Session = Depends(get_db)):
    chat_exist = crud.get_chat(db, chatid=chat_id)
    if not chat_exist:
        raise HTTPException(status_code=400, detail="Chat Doesn't exists")

    chatcontentsid = chat_id + ctime()

    chatContentsTable = schemas.ChatContentsTableCreate(
        chatcontentsid =  chatcontentsid,
        chatid =  chat_id,
        senderid =  chat_content.senderid,
        message =  chat_content.message,
    )

    crud.create_chat_content(db=db, chat_content=chatContentsTable)

    #RAG 답변 생성해서 넣기
    db_ai = crud.get_ai(db, aiid=chat_exist.aiid)

    # token, answer = rag_qa(chat_content.message, chat_exist.aiid)
    token, answer = rag_qa(chat_content.message, "dating_adivce_ai")

    aiUpdateDB = schemas.AITableUsageUpdate(
        usage = db_ai.usage + token.completion_tokens,
        total_usage = db_ai.usage + token.total_tokens,
        collect = db_ai.collect + db_ai.ratio * token.completion_tokens
    )
    
    crud.update_usage_ai(db=db, aiid=chat_exist.aiid, ai_update=aiUpdateDB)


    chatcontentsid = "AI_" + chat_id + ctime()

    answerContentsTable = schemas.ChatContentsTableCreate(
        chatcontentsid =  chatcontentsid,
        chatid =  chat_id,
        senderid =  chat_exist.aiid,
        message =  answer,
    )

    return crud.create_chat_content(db=db, chat_content=answerContentsTable)

# 특정 채팅 내용 읽기
@app.get("/chatcontents/{chat_id}", response_model=schemas.ChatContentsTableListOut)
def read_chat_content(chat_id: str, db: Session = Depends(get_db)):
    db_chat_content = crud.get_chat_contents(db, chat_id=chat_id)

    return schemas.ChatContentsTableListOut(chats=db_chat_content)

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


## COLLECT MONEY


@app.post("/login/", response_model=schemas.UserTableBase)
def login_or_create_user(user: schemas.UserTableCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, userid=user.userid)
    if db_user:
        return db_user  # 사용자가 이미 존재하면 사용자 정보 반환
    else:
        # 사용자가 존재하지 않으면 새로 생성
        return crud.create_user(db=db, user=user)

# 사용자 정보 업데이트
@app.put("/user/{userid}", response_model=schemas.UserTableBase)
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

# AI로 번 돈 받기
@app.post("/collect/{aiid}", response_model=schemas.AITableBase)
def create_ai(aiid : str, db: Session = Depends(get_db)):
    #먼저 만들어졌었는지 확인
    print(aiid)
    db_ai = crud.get_ai(db, aiid=aiid)
    if not db_ai:
        raise HTTPException(status_code=400, detail="AI Not exists")
    
    ##블록체인 쏘기
    
    aiUpdateDB = schemas.AITableCollectUpdate(
        collect = 0
    )

    return crud.update_usage_ai(db=db, aiid=aiid, ai_update=aiUpdateDB)
