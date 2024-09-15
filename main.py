from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
import requests
from sqlalchemy.orm import Session

from DB import users, ais, chats, models, schemas
from DB.database import SessionLocal, engine

from AI.crud import add_text, delete_text
from AI.main import rag_qa
from fastapi.middleware.cors import CORSMiddleware

from SUI import suiapi

import random
from time import ctime


# 데이터베이스 테이블 생성하기
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5000", 'https://nearanddear.ysblockblock.com'],  # 허용할 클라이언트의 도메인
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메서드 (GET, POST, OPTIONS 등)
    allow_headers=["*"],  # 허용할 헤더
)

BASE_URL = "http://localhost:8080"
RAGCOON_STAGE_ID = "0x68e7482eb88d2bfe57481a8078ed447bc50c00f7487d9484bc00b9e49c0c7986"
headers = {"Content-Type": "application/json"}


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

########################### 유저 관련 API ###########################
@app.get("/users/{offset}/{limit}", response_model=List[schemas.UserTableBase])
def get_users(offset : int, limit : int, db: Session = Depends(get_db)):
    return users.get_users(db=db, offset=offset, limit=limit)

@app.get("/users/{user_address}", response_model=schemas.UserTableBase)
def get_user(user_address : str, db: Session = Depends(get_db)):
    return users.get_user(db, user_address=user_address)

@app.get("/users/exists/{user_address}", response_model=bool)
def check_user_exists(user_address : str, db: Session = Depends(get_db)):
    res = users.check_user_exists(db = db, user_address=user_address)
    return res

@app.post("/users", response_model=schemas.UserTableBase)
def add_user(user: schemas.UserTableCreate, db: Session = Depends(get_db)):
    suiapi.add_user_creator_consumser(user.user_address)
    return users.add_user(db, user = user)

# @app.put("/users", response_model=schemas.UserTableBase)
# def update_user(user: schemas.UserTableCreate, db: Session = Depends(get_db)):
#     return users.update_user(db, user = user)

########################### AI 관련 API ###########################

@app.get("/ais/{offset}/{limit}", response_model=schemas.AITableListOut)
def get_ais(offset: int, limit: int, db: Session = Depends(get_db)):
    res = ais.get_ais(db=db, offset=offset, limit=limit)
    return schemas.AITableListOut(ais=res)

@app.get("/ais/{ai_id}", response_model=schemas.AIDetail)
def get_ai(ai_id: str, db: Session = Depends(get_db)):
    db_ai = ais.get_ai_detail(db, ai_id=ai_id)
    if not db_ai:
        raise HTTPException(status_code=404, detail="AI not found")
    return db_ai

@app.get("/ais/{user_address}", response_model=schemas.AITableListOut)
def get_user_ais(user_address: str, db: Session = Depends(get_db)):
    res = ais.get_user_ais(db=db, user_address=user_address)
    return schemas.AITableListOut(ais=res)

@app.get("/ais/{ai_id}/rags", response_model=schemas.RAGTableListOut)
def get_rags(ai_id: str, db: Session = Depends(get_db)):
    res = ais.get_rags(db=db, ai_id=ai_id)
    return schemas.RAGTableListOut(logs=res)

#인기있는 AI 보기
@app.get("/ais/trend/{category}/{offset}/{limit}", response_model=schemas.AITableListOut)
def get_trend_ais(category : str, offset : int, limit : int, db: Session = Depends(get_db), ):
    if category == "all":
        res =  ais.get_ais_by_weekly_users(db=db, offset=offset, limit=limit)
        return schemas.AITableListOut(ais=res)
    else:
        res = ais.get_category_ais_by_weekly_users(db=db, offset=offset, limit=limit, category=category)
        return schemas.AITableListOut(ais=res)

@app.get("/ais/today", response_model=schemas.AITableListOut)
def get_today_ais(db: Session = Depends(get_db)):
    res =  ais.get_today_ais(db=db)
    return schemas.AITableListOut(ais=res)  

@app.get("/ais/search/{ai_name}", response_model=schemas.AISearchListOut)
def search_ai(ai_name: str, db: Session = Depends(get_db)):
    db_ai = ais.search_ai(db, name=ai_name)
    if not db_ai:
        raise HTTPException(status_code=404, detail="AI not found")
    search_results = [
        schemas.AISearch(
            name=ai.name,
            creator_address=ai.creator_address,
            image_url=ai.image_url
        ) for ai in db_ai
    ]
    return schemas.AISearchListOut(ais=search_results)

@app.post("/ais", response_model=schemas.AITableBase)
def create_ai(ai: schemas.AITableCreate, db: Session = Depends(get_db)):
    ai_id = ai.creator_address + '_' + ai.name

    #먼저 만들어졌었는지 확인
    db_ai = ais.get_ai(db, ai_id=ai_id)
    if db_ai:
        raise HTTPException(status_code=400, detail="AI with this ID already exists")

    db_user = ais.get_user(db, user_address=ai.creator_address)
    if not db_user:
        raise HTTPException(status_code=400, detail="You are not user")
    
    faiss_id = ai.name + "tx" + str(random.random())

    # AI 콘텐츠를 추가하는 로직
    embed = add_text([ai.contents], [{"source" : ai_id}], [faiss_id])

    # 블록체인에 ai 생성
    suiapi.add_ai(ai_id=ai_id, creator_address=ai.creator_address)

    # blov 저장
    digest = suiapi.add_blob(ai=ai, embed=embed)
    
    # AILog 테이블에 로그 기록
    ais.create_rag(db=db, ai_id=ai_id, comments=ai.comments, digest=digest, faiss_id=faiss_id)
    
    return ais.create_ai(db=db, ai_id=ai_id, ai=ai)

@app.put("/ais", response_model= schemas.AITableBase)
def update_ais(ai_update: schemas.AITableUserUpdateInput,db: Session = Depends(get_db)):
    db_ai = ais.get_ai(db, ai_id=ai_update.ai_id)
    if not db_ai:
        raise HTTPException(status_code=400, detail="AI Not found")
    if db_ai.creator_address != ai_update.user_address:
        raise HTTPException(status_code=400, detail="You are not the owner of AI")

    # AI 콘텐츠가 변경된 경우 add_text 호출
    if ai_update.contents != "":
        faiss_id = db_ai.name + "tx" + str(random.random())
        embed = add_text([ai_update.contents], [{"source" : db_ai.ai_id}], [faiss_id])

        digest = suiapi.add_blob(ai=db_ai, embed=embed)

        ais.create_rag(db=db, ai_id=ai_update.ai_id, comments=ai_update.comments, digest=digest, faiss_id=faiss_id)
    
    return ais.update_ai(db=db, ai_id=ai_update.ai_id, ai_update=ai_update)

@app.delete("/ais/{ai_id}/{user_address}", response_model=schemas.AITableBase)
def delete_ai(ai_id: str, user_address: str, db: Session = Depends(get_db)):

    db_ai = ais.get_ai(db, ai_id=ai_id)
    if not db_ai:
        raise HTTPException(status_code=404, detail="AI not found")
    if db_ai.creator_address != user_address:
        raise HTTPException(status_code=400, detail="You are not the owner of AI")
    
    deleted_ai = ais.delete_ai(db=db, ai_id=ai_id)

    ai_logs = ais.get_raglogs_by_aiid(db=db, ai_id=ai_id)
    ids = [i.faiss_id for i in ai_logs]
    delete_text(ids)

    ais.delete_raglogs(db=db, ai_id=ai_id)

    if not deleted_ai:
        raise HTTPException(status_code=404, detail="AI not found")
    return deleted_ai

# #특정 AI 로그 목록 보기
# @app.get("/ailogs/ai/{aiid}", response_model=schemas.AILogTableListOut)
# def read_ailog_by_aiid(aiid: str, db: Session = Depends(get_db)):
#     db_ailogs = ais.get_ailogs_by_aiid(db, aiid=aiid)
#     if not db_ailogs:
#         raise HTTPException(status_code=404, detail="Log not found")
#     return schemas.AILogTableListOut(logs=db_ailogs)

########################### Chat 관련 API ###########################

# # 유저 채팅 목록 읽기
@app.get("/chats/{user_address}", response_model=schemas.ChatTableListOut)
def get_chats(user_address: str, db: Session = Depends(get_db)):
    db_chat = chats.get_chats(db, user_address=user_address)
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return schemas.ChatTableListOut(chats=db_chat)

@app.get("/chats/{ai_id}", response_model=schemas.ChatTableListOut)
def get_chats(ai_id: str, db: Session = Depends(get_db)):
    db_chat = chats.get_chats(db, ai_id=ai_id)
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return schemas.ChatTableListOut(chats=db_chat)
    
# # 특정 채팅 읽기
@app.get("/chats/contents/{chat_id}", response_model=schemas.ChatContentsTableListOut)
def read_chat_content(chat_id: str, db: Session = Depends(get_db)):
    db_chat_content = chats.get_chat_contents(db, chat_id=chat_id)

    return schemas.ChatContentsTableListOut(chats=db_chat_content)

# # 챗 생성
@app.post("/chats", response_model=schemas.ChatTableBase)
def create_chat(chat: schemas.ChatTableCreate, db: Session = Depends(get_db)):
    db_ai = chats.get_ai(db, ai_id=chat.ai_id)
    if not db_ai:
        raise HTTPException(status_code=404, detail="AI not found")

    chat_id = chat.user_address + '_' + chat.ai_id

    chat_exist = chats.get_chat(db, chat_id=chat_id)
    if chat_exist:
        raise HTTPException(status_code=400, detail="Chat already exists")

    chatTable = schemas.ChatTableBase(
        chat_id=chat_id,
        user_address=chat.user_address,
        ai_id= chat.ai_id,
    )

    return chats.create_chat(db=db, chat=chatTable)


# # 채팅 내용 생성
@app.post("/chats/contents/{chat_id}", response_model=schemas.ChatContentsTableBase)
def create_chat_content(chat_content: schemas.ChatContentsTableCreateInput, chat_id :str, db: Session = Depends(get_db)):
    chat_exist = chats.get_chat(db, chat_id=chat_id)
    if not chat_exist:
        raise HTTPException(status_code=400, detail="Chat Doesn't exists")

    chatcontentsid = chat_id + '_' + ctime()

    chatContentsTable = schemas.ChatContentsTableCreate(
        chat_contents_id =  chatcontentsid,
        chat_id =  chat_id,
        sender_id =  chat_content.sender_id,
        message =  chat_content.message,
    )

    chats.create_chat_content(db=db, chat_content=chatContentsTable)

    #RAG 답변 생성해서 넣기
    db_ai = chats.get_ai(db, ai_id=chat_exist.ai_id)

    token, answer = rag_qa(chat_content.message, chat_exist.ai_id)
    # token, answer = rag_qa(chat_content.message, "dating_adivce_ai")

    aiUpdateDB = schemas.AITableUsageUpdate(
        chat_counts= db_ai.chat_counts + 1,
        prompt_tokens = db_ai.prompt_tokens + token.prompt_tokens,
        completion_tokens = db_ai.completion_tokens + token.completion_tokens,
    )
    
    chats.update_usage_ai(db=db, ai_id=chat_exist.ai_id, ai_update=aiUpdateDB)


    chatcontentsid = "AI_" + chat_id + ctime()

    answerContentsTable = schemas.ChatContentsTableCreate(
        chat_contents_id =  chatcontentsid,
        chat_id=  chat_id,
        sender_id =  chat_exist.ai_id,
        message =  answer,
    )

    suiapi.pay_usage(ai=db_ai, tokens=token.prompt_tokens)

    return chats.create_chat_content(db=db, chat_content=answerContentsTable)

# # 채팅 삭제
# @app.delete("/chats/{chat_id}", response_model=schemas.ChatTableBase)
# def delete_chat(chat_id: str, db: Session = Depends(get_db)):
#     deleted_chat = chats.delete_chat(db=db, chat_id=chat_id)
#     if not deleted_chat:
#         raise HTTPException(status_code=404, detail="Chat not found")
#     return deleted_chat