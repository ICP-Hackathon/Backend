from sqlalchemy import Column, Integer, String, Time, Text, Float, func, DateTime, Boolean
from datetime import datetime
from DB.database import Base

class UserTable(Base):
    __tablename__ = "usertable"

    user_address = Column(String, nullable=False, primary_key=True)
    nickname = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    country = Column(String, nullable=False)
    interest = Column(String, nullable=False)
    profile_image_url = Column(String, nullable=False)

class AITable(Base):
    __tablename__ = "aitable"

    id = Column(String, nullable=False, primary_key=True)
    creator_address = Column(String, nullable=False)
    name = Column(String, nullable=False)
    profile_image_url = Column(String, nullable=False)
    category = Column(String, nullable=False)
    introductions = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)  # Use DateTime instead of String

class RAGTable(Base):
    __tablename__ = "ragtable"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ai_id = Column(String, primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=True)  # Use DateTime instead of String
    comments = Column(Text, nullable=True)
    tx_url = Column(String, nullable=True)
    is_stored_at_blockchain = Column(Boolean, nullable=False)
    faiss_id = Column(String, nullable=True)

class ChatTable(Base):
    __tablename__ = "chattable"

    id = Column(String, nullable=False, primary_key=True)
    ai_id = Column(String, nullable=False)
    user_address = Column(String, nullable=False)
    daily_user_access = Column(Boolean, nullable=True)


class ChatContentsTable(Base):
    __tablename__ = "chatcontentstable"

    id = Column(String, nullable=False, primary_key=True)
    chat_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=True)  # Use DateTime instead of String
    sender_id = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    prompt_tokens = Column(Float, nullable=True)
    completion_tokens = Column(Float, nullable=True)

class LikeTable(Base):
    __tablename__ = "liketable"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_address = Column(String, nullable=True)
    ai_id = Column(String, nullable=True)
    like = Column(Boolean, nullable=False)