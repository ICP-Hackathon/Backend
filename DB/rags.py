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
