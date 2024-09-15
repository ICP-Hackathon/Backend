from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request
import requests
from sqlalchemy.orm import Session

from DB import crud, models, schemas
from DB.database import SessionLocal, engine

from AI.crud import add_text, delete_text
from AI.main import rag_qa
from fastapi.middleware.cors import CORSMiddleware

from Walrus.main import send_data


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

@app.get("/check_user/{user_address}", response_model=bool)
def check_user(user_address : str, db: Session = Depends(get_db)):
    res = crud.check_user(db = db, user_address=user_address)
    return res

@app.get("/get_user/{user_address}", response_model=schemas.UserTableBase)
def get_user(user_address : str, db: Session = Depends(get_db)):
    return crud.get_user(db, user_address=user_address)

@app.post("/add_user/", response_model=schemas.UserTableBase)
def add_user(user: schemas.UserTableCreate, db: Session = Depends(get_db)):
    creator_url = BASE_URL + "/movecall/add_creator"
    consumer_url = BASE_URL + "/movecall/add_consumer"
    creator_params = {
        "ragcoonStageId": RAGCOON_STAGE_ID,
        "creatorAddress": user.user_address,
    }
    consumer_paramse = {
        "ragcoonStageId": RAGCOON_STAGE_ID,
        "consumerAddress": user.user_address,
    }
    # Make the POST request to another API with the received data
    creator_response = requests.get(creator_url, params=creator_params, headers=headers).json()
    consumer_response = requests.get(consumer_url, params=consumer_paramse, headers=headers).json()

    print("Creator Response")
    print(creator_response)
    
    print("Consumer Response")
    print(consumer_response)

    userDB = schemas.UserTableBase(
        user_address = user.user_address,
        nickname = user.nickname,
        image_url = user.image_url,
        gender = user.gender,
        country = user.country,
        phone= user.phone,
        creator_id = creator_response.get(''),
        consumer_id = consumer_response.get('')
    )


    return crud.add_user(db, user = user)


# 사용자 정보 업데이트
# @app.put("/update_user", response_model=schemas.UserTableBase)
# def update_user(user_update: schemas.UserTableUpdate, db: Session = Depends(get_db)):
#     updated_user = crud.update_user(db=db, user_update=user_update)
#     if not updated_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return updated_user

# 사용자 삭제
# @app.delete("/user/{userid}", response_model=schemas.UserTableOut)
# def delete_user(userid: str, db: Session = Depends(get_db)):
#     deleted_user = crud.delete_user(db=db, userid=userid)
#     if not deleted_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return deleted_user


########################### AI 관련 API ###########################

#인기있는 AI 보기
@app.get("/get_trend_ais/{category}/{offset}/{limit}", response_model=schemas.AITableListOut)
def get_trend_ais(category : str, offset : int, limit : int, db: Session = Depends(get_db), ):
    if category == "all":
        res =  crud.get_ais_by_weekly_users(db=db, offset=offset, limit=limit)
        return schemas.AITableListOut(ais=res)
    else:
        res = crud.get_category_ais_by_weekly_users(db=db, offset=offset, limit=limit, category=category)
        return schemas.AITableListOut(ais=res)

@app.get("/today_ais", response_model=schemas.AITableListOut)
def get_today_ais(db: Session = Depends(get_db)):
    res =  crud.get_today_ais(db=db)
    return schemas.AITableListOut(ais=res)  
    

@app.get("/search_ais/{ai_name}", response_model=schemas.AISearchListOut)
def search_ai(ai_name: str, db: Session = Depends(get_db)):
    db_ai = crud.search_ai(db, name=ai_name)
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


@app.post("/create_ai/", response_model=schemas.AITableBase)
def create_ai(ai: schemas.AITableCreate, db: Session = Depends(get_db)):
    add_ai_url = BASE_URL + "/movecall/add_ai"  # The URL of the REST API you want to call
    add_blob_url = BASE_URL + "/movecall/add_blob_id"  # The URL of the REST API you want to call

    ai_id = ai.creator_address + '_' + ai.name


    #먼저 만들어졌었는지 확인
    db_ai = crud.get_ai(db, ai_id=ai_id)
    if db_ai:
        raise HTTPException(status_code=400, detail="AI with this ID already exists")

    db_user = crud.get_user(db, user_address=ai.creator_address)
    if not db_user:
        raise HTTPException(status_code=400, detail="You are not user")
    
    faiss_id = ai.name + "tx" + str(random.random())

    # AI 콘텐츠를 추가하는 로직
    embed = add_text([ai.contents], [{"source" : ai_id}], [faiss_id])
    res = send_data(str(embed))
    blob_id = ''
    if 'newlyCreated' in res :
        blob_id = res['newlyCreated']['blobObject']['blobId']
    elif 'alreadyCertified' in res :
        blob_id = res['alreadyCertified']['blobId']    
    # Extract necessary data from the request (example)

    add_ai_params = {
        "ragcoonStageId": RAGCOON_STAGE_ID,
        "creatorAddress": ai.creator_address,
        "AIID" : ai_id,
    }

    response1 = requests.get(add_ai_url, params=add_ai_params, headers=headers).json()
    # digest1 = response1.get('digest')

    add_blob_params = {
        "ragcoonStageId": RAGCOON_STAGE_ID,
        "creatorAddress": ai.creator_address,
        "AIID" : ai_id,
        "blobID" : blob_id
    }
    # Make the POST request to another API with the received data
    response2 = requests.get(add_blob_url, params=add_blob_params, headers=headers).json()
    digest = response2.get('digest')


    aiDB = schemas.AITableBase(
        ai_id = ai_id,
        creator_address =  ai.creator_address,
        created_at = datetime.now(),
        name = ai.name,
        image_url = ai.image_url,
        category = ai.category,
        introductions = ai.introductions,
        chat_counts=0,
        prompt_tokens=0,
        completion_tokens=0,
        weekly_users = 0
        )

#     # AI 테이블에 새로운 항목 생성
    created_ai = crud.create_ai(db=db, ai=aiDB)
    
    # AILog 테이블에 로그 기록
    rag = schemas.RAGTableCreate(
        ai_id = ai_id,
        created_at = ctime(),
        comments =ai.comments,
        tx_url= digest,
        faissid = faiss_id
    )
    crud.create_rag(db=db, rag=rag)
    
    return created_ai

# AI 정보 업데이트
@app.put("/update_ai/", response_model=schemas.AITableBase)
def update_ai(ai_update: schemas.AITableUserUpdateInput, db: Session = Depends(get_db)):
    db_ai = crud.get_ai(db, ai_id=ai_update.ai_id)
    if not db_ai:
        raise HTTPException(status_code=400, detail="AI Not found")
    if db_ai.creator_address != ai_update.user_address:
        raise HTTPException(status_code=400, detail="You are not the owner of AI")

    # AI 콘텐츠가 변경된 경우 add_text 호출
    if ai_update.contents != "":
        faiss_id = db_ai.name + "tx" + str(random.random())
        embed = add_text([ai_update.contents], [{"source" : db_ai.ai_id}], [faiss_id])
        res = send_data(str(embed))
        blob_id = ''
        if 'newlyCreated' in res :
            blob_id = res['newlyCreated']['blobObject']['blobId']
        elif 'alreadyCertified' in res :
            blob_id = res['alreadyCertified']['blobId']

        url = BASE_URL + "/movecall/add_blob_id"  # The URL of the REST API you want to call
        headers = {"Content-Type": "application/json"}
        params = {
            "ragcoonStageId": "0x6cf0caaed681c010a3466a6c0c9ea6169b114c25ad708193f2dec506b1a35b70",
            "creatorID": "db",
            "AIID" : db_ai.ai_id,
            "blobID" : blob_id
        }
        # Make the POST request to another API with the received data
        response = requests.get(url, params=params, headers=headers).json()
        digest = (response.get('digest'))
            
        # AILog 테이블에 로그 기록
        rag = schemas.RAGTableCreate(
            ai_id = ai_update.ai_id,
            created_at = ctime(),
            comments =ai_update.comments,
            tx_url= digest,
            faissid = faiss_id
        )

        crud.create_rag(db=db, rag=rag)
    
    aiUpdateDB = schemas.AITableUpdate(
        name = ai_update.name,
        image_url = ai_update.image_url,
        category= ai_update.category,  # 카테고리 필드, None이 기본값
        introductions=ai_update.introductions  # 소개 필드, None이 기본값
    )

    # AI 정보를 업데이트
    updated_ai = crud.update_ai(db=db, ai_id=ai_update.ai_id, ai_update=aiUpdateDB)
    
    return updated_ai


# # 내 AI 보기
@app.get("/get_my_ais/{user_address}", response_model=schemas.AITableListOut)
def read_my_ais(user_address : str, db: Session = Depends(get_db)):
    res =  crud.get_user_ais(db=db, user_address=user_address)
    return schemas.AITableListOut(ais=res)
# # 특정 AI 읽기
@app.get("/get_ai_detail/{ai_id}", response_model=schemas.AIDetail)
def read_ai(ai_id: str, db: Session = Depends(get_db)):
    db_ai = crud.get_ai_detail(db, ai_id=ai_id)
    if not db_ai:
        raise HTTPException(status_code=404, detail="AI not found")
    return db_ai

# AI 삭제
@app.delete("/delete_ai/{ai_id}/{user_address}", response_model=schemas.AITableBase)
def delete_ai(ai_id: str, user_address: str, db: Session = Depends(get_db)):

    db_ai = crud.get_ai(db, ai_id=ai_id)
    if not db_ai:
        raise HTTPException(status_code=404, detail="AI not found")
    if db_ai.creator_address != user_address:
        raise HTTPException(status_code=400, detail="You are not the owner of AI")
    
    deleted_ai = crud.delete_ai(db=db, ai_id=ai_id)

    ai_logs = crud.get_raglogs_by_aiid(db=db, ai_id=ai_id)
    ids = [i.faiss_id for i in ai_logs]
    delete_text(ids)

    crud.delete_raglogs(db=db, ai_id=ai_id)

    if not deleted_ai:
        raise HTTPException(status_code=404, detail="AI not found")
    return deleted_ai

# #특정 AI 로그 목록 보기
# @app.get("/ailogs/ai/{aiid}", response_model=schemas.AILogTableListOut)
# def read_ailog_by_aiid(aiid: str, db: Session = Depends(get_db)):
#     db_ailogs = crud.get_ailogs_by_aiid(db, aiid=aiid)
#     if not db_ailogs:
#         raise HTTPException(status_code=404, detail="Log not found")
#     return schemas.AILogTableListOut(logs=db_ailogs)

# # 채팅 생성
@app.post("/chats/", response_model=schemas.ChatTableBase)
def create_chat(chat: schemas.ChatTableCreate, db: Session = Depends(get_db)):
    db_ai = crud.get_ai(db, ai_id=chat.ai_id)
    if not db_ai:
        raise HTTPException(status_code=404, detail="AI not found")

    chat_id = chat.user_address + '_' + chat.ai_id

    chat_exist = crud.get_chat(db, chat_id=chat_id)
    if chat_exist:
        raise HTTPException(status_code=400, detail="Chat already exists")

    chatTable = schemas.ChatTableBase(
        chat_id=chat_id,
        user_address=chat.user_address,
        ai_id= chat.ai_id,
    )

    return crud.create_chat(db=db, chat=chatTable)

# # 유저 채팅 목록 읽기
@app.get("/chats/{user_address}", response_model=schemas.ChatTableListOut)
def read_chat(user_address: str, db: Session = Depends(get_db)):
    db_chat = crud.get_chats(db, user_address=user_address)
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return schemas.ChatTableListOut(chats=db_chat)

# # 채팅 삭제
# @app.delete("/chats/{chat_id}", response_model=schemas.ChatTableBase)
# def delete_chat(chat_id: str, db: Session = Depends(get_db)):
#     deleted_chat = crud.delete_chat(db=db, chat_id=chat_id)
#     if not deleted_chat:
#         raise HTTPException(status_code=404, detail="Chat not found")
#     return deleted_chat

# # 채팅 내용 생성
@app.post("/chatcontent/{chat_id}", response_model=schemas.ChatContentsTableBase)
def create_chat_content(chat_content: schemas.ChatContentsTableCreateInput, chat_id :str, db: Session = Depends(get_db)):
    chat_exist = crud.get_chat(db, chat_id=chat_id)
    if not chat_exist:
        raise HTTPException(status_code=400, detail="Chat Doesn't exists")

    chatcontentsid = chat_id + '_' + ctime()

    chatContentsTable = schemas.ChatContentsTableCreate(
        chat_contents_id =  chatcontentsid,
        chat_id =  chat_id,
        sender_id =  chat_content.sender_id,
        message =  chat_content.message,
    )

    crud.create_chat_content(db=db, chat_content=chatContentsTable)

    #RAG 답변 생성해서 넣기
    db_ai = crud.get_ai(db, ai_id=chat_exist.ai_id)

    token, answer = rag_qa(chat_content.message, chat_exist.ai_id)
    # token, answer = rag_qa(chat_content.message, "dating_adivce_ai")

    aiUpdateDB = schemas.AITableUsageUpdate(
        chat_counts= db_ai.chat_counts + 1,
        prompt_tokens = db_ai.prompt_tokens + token.prompt_tokens,
        completion_tokens = db_ai.completion_tokens + token.completion_tokens,
    )
    
    crud.update_usage_ai(db=db, ai_id=chat_exist.ai_id, ai_update=aiUpdateDB)


    chatcontentsid = "AI_" + chat_id + ctime()

    answerContentsTable = schemas.ChatContentsTableCreate(
        chat_contents_id =  chatcontentsid,
        chat_id=  chat_id,
        sender_id =  chat_exist.ai_id,
        message =  answer,
    )

    return crud.create_chat_content(db=db, chat_content=answerContentsTable)

# # 특정 채팅 내용 읽기
@app.get("/chatcontents/{chat_id}", response_model=schemas.ChatContentsTableListOut)
def read_chat_content(chat_id: str, db: Session = Depends(get_db)):
    db_chat_content = crud.get_chat_contents(db, chat_id=chat_id)

    return schemas.ChatContentsTableListOut(chats=db_chat_content)

# ## COLLECT MONEY

# # AI로 번 돈 받기
# @app.post("/collect/{aiid}", response_model=schemas.AITableBase)
# def create_ai(aiid : str, db: Session = Depends(get_db)):
#     #먼저 만들어졌었는지 확인
#     print(aiid)
#     db_ai = crud.get_ai(db, aiid=aiid)
#     if not db_ai:
#         raise HTTPException(status_code=400, detail="AI Not exists")
    
#     ##블록체인 쏘기
    
#     aiUpdateDB = schemas.AITableCollectUpdate(
#         collect = 0
#     )

#     return crud.update_usage_ai(db=db, aiid=aiid, ai_update=aiUpdateDB)
