from typing import List

from sqlalchemy.orm import Session
from DB import models
from Schema import base_schemas, rag_schemas
from datetime import datetime

def create_rag(db: Session, ai_id: str, comments: str, tx_hash: str, faiss_id: str):
    rag = rag_schemas.RAGCreate(
        ai_id = ai_id,
        comments = comments,
        tx_hash = tx_hash,
        faiss_id = faiss_id,
    )
    db_rag = models.RAGTable(**rag.model_dump())
    db.add(db_rag)
    db.commit()
    db.refresh(db_rag)

def get_rags_by_aiid(db: Session, ai_id: str):
    return db.query(models.RAGTable).filter(models.RAGTable.ai_id == ai_id).all()

def delete_raglogs(db: Session, ai_id: str):
    # AI ID와 관련된 모든 로그를 가져옴
    ailogs = get_rags_by_aiid(db, ai_id)

    if not ailogs:
        return None  # 로그가 없으면 None 반환

    # 각 로그를 순회하며 삭제
    for log in ailogs:
        db.delete(log)

    # 모든 로그를 삭제한 후 commit
    db.commit()

    return ailogs  # 삭제된 로그 목록 반환