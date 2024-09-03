from sqlalchemy import Column, Integer, String, DateTime, Sequence, Date
from DB.database import Base
from datetime import datetime

# Base를 상속 받아 SQLAlchemy model 생성
class Profile(Base):
    __tablename__ = "profiles"

    user_name = Column(String, nullable=False, name="user", primary_key=True)
    name = Column(String, nullable=True)
    sex = Column(String, nullable=True)
    birth = Column(Date, nullable=True)
    mbti = Column(String, nullable=True)
    keywords = Column(String, nullable=True)
    contents = Column(String, nullable=True)

class DiaryModel(Base):
    __tablename__ = "diary"

    id = Column(Integer, Sequence('diary_id_seq'), primary_key=True, index=True)
    date = Column(DateTime, nullable=True, default=datetime.utcnow)  # timestamp 타입의 date 필드, 기본값은 현재 시간
    keywords = Column(String, nullable=True)
    contents = Column(String, nullable=True)
    happy = Column(Integer, nullable=True)
    sad = Column(Integer, nullable=True)
    love = Column(Integer, nullable=True)
    user_name = Column(String, nullable=False, name="user")