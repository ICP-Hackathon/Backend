from sqlalchemy import Column, Integer, String, Time, Text, Float, func, DateTime
from datetime import datetime
from DB.database import Base

class UserTable(Base):
    __tablename__ = "usertable"

    user_address = Column(String, nullable=False, primary_key=True)
    image_url = Column(String, nullable=True)
    nickname = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    country = Column(String, nullable=True)
    phone = Column(String, nullable=True)

class AITable(Base):
    __tablename__ = "aitable"

    ai_id = Column(String, nullable=False, primary_key=True)
    creator_address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=True)  # Use DateTime instead of String
    name = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    category = Column(String, nullable=True)
    introductions = Column(String, nullable=True)
    chat_counts = Column(Integer, nullable=True)
    prompt_tokens = Column(Float, nullable=True)
    completion_tokens = Column(Float, nullable=True)
    weekly_users = Column(Integer, nullable=True)

class RAGTable(Base):
    __tablename__ = "ragtable"

    rag_id = Column(Integer, primary_key=True, autoincrement=True)
    ai_id = Column(String, primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=True)  # Use DateTime instead of String
    comments = Column(Text, nullable=True)
    tx_url = Column(String, nullable=True)
    faiss_id = Column(String, nullable=True)

class ChatTable(Base):
    __tablename__ = "chattable"

    chat_id = Column(String, nullable=False, primary_key=True)
    ai_id = Column(String, nullable=False)
    user_address = Column(String, nullable=False)

class ChatContentsTable(Base):
    __tablename__ = "chatcontentstable"

    chat_contents_id = Column(String, nullable=False, primary_key=True)
    chat_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=True)  # Use DateTime instead of String
    sender_id = Column(String, nullable=True)
    message = Column(Text, nullable=True)