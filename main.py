from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

# from DB import users, ais, chats, models, schemas, like
from DB import models
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
    allow_origins=["http://localhost:3000", "http://localhost:5000", 'https://suietail.ysblockblock.com'],  # 허용할 클라이언트의 도메인
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