from sqlalchemy import Column, Integer, String, Time, Text, func
from DB.database import Base

class UserTable(Base):
    __tablename__ = "usertable"

    userid = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=True)
    profileimage = Column(String, nullable=True)

class AITable(Base):
    __tablename__ = "aitable"

    id = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=True)
    category = Column(String, nullable=True)
    introductions = Column(String, nullable=True)
    usage = Column(Integer, nullable=True, default=0)
    total_usage = Column(Integer, nullable=True, default = 0)
    ratio = Column(Integer, nullable=True, default = 0)

class AILogTable(Base):
    __tablename__ = "ailogtable"

    id = Column(Integer, primary_key=True, autoincrement=True)
    aiid = Column(String, nullable=True)
    createdat = Column(Time, nullable=True, default=func.current_timestamp())
    log = Column(Text, nullable=True)
    txurl = Column(String, nullable=True)

class ChatTable(Base):
    __tablename__ = "chattable"

    chatid = Column(String, nullable=False, primary_key=True)
    aiid = Column(String, nullable=True)
    userid = Column(String, nullable=True)

class ChatContentsTable(Base):
    __tablename__ = "chatcontentstable"

    chatcontentsid = Column(String, nullable=False, primary_key=True)
    chatid = Column(String, nullable=True)
    createdat = Column(Time, nullable=True, default=func.current_timestamp())
    senderid = Column(String, nullable=True)
    message = Column(Text, nullable=True)