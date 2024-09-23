from DB.database import SessionLocal
from time import ctime

# 종속성 만들기: 요청 당 독립적인 데이터베이스 세션/연결이 필요하고 요청이 완료되면 닫음
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_ai_id(creator_address: str, ai_name: str ) -> str:
    return creator_address + '_' + ai_name

def create_chat_id(user_address: str, ai_id: str ) -> str:
    return user_address + '_' + ai_id

def create_chat_message_id(chat_id) -> str:
    return 'AI_' + chat_id + '_' + ctime()