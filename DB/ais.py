from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from .like import check_like
from .users import get_user
from .chats import check_chat_by_ai_id
from sqlalchemy import func


################### AITable CRUD functions ###################

def get_ais(db: Session, offset: int, limit: int):
    # AITable에서 offset과 limit을 사용하여 AI 목록을 가져옴
    ai_infos = db.query(models.AITable).offset(offset).limit(limit - offset).all()

    ai_overview_list = []  # 결과를 담을 리스트

    # 각 ai_info에 대해 처리
    for ai_info in ai_infos:
        # 유저 정보를 가져옴
        creator_info = get_user(db=db, user_address=ai_info.creator_address)

        # 유저가 해당 AI를 좋아하는지 여부를 확인
        like_bool = check_like(db=db, user_address=creator_info.user_address, ai_id=ai_info.ai_id)

        # AIOverview 객체 생성
        ai_overview = schemas.AIOverview(
            ai_id=ai_info.ai_id,
            creator_address=ai_info.creator_address,
            ai_name=ai_info.ai_name,
            creator=creator_info.nickname,  # 유저 닉네임을 가져옴
            like=like_bool,  # 유저가 AI를 좋아하는지 여부
            image_url= ai_info.image_url,
            category= ai_info.category
        )

        # 리스트에 추가
        ai_overview_list.append(ai_overview)

    # 최종 결과로 AIOVerviewList 반환
    return schemas.AIOVerviewList(ais=ai_overview_list)

def get_ai(db: Session, ai_id: str):
    return db.query(models.AITable).filter(models.AITable.ai_id == ai_id).first()
    

def get_user_ais(db: Session, user_address: str):
    # 유저가 만든 AI 리스트를 가져옵니다
    ai_infos = db.query(models.AITable).filter(models.AITable.creator_address == user_address).all()

    my_ais_list = []  # 각 ai_info에 대한 MyAIsOut 객체를 담을 리스트

    for ai_info in ai_infos:
        # 각 ai_info에 대한 usage(토큰 사용량) 계산
        check_chat = check_chat_by_ai_id(db=db, ai_id=ai_info.ai_id)
        if check_chat:
            usage = db.query(
                func.sum(models.ChatContentsTable.prompt_tokens + models.ChatContentsTable.completion_tokens))\
                .join(models.ChatTable, models.ChatContentsTable.chat_id == models.ChatTable.chat_id)\
                .filter(models.ChatTable.ai_id == ai_info.ai_id)\
                .scalar()
            print(usage)
            # 만약 usage 값이 None이면 0으로 설정 (사용 기록이 없을 때 대비)
            usage = usage or 0
        else:
            usage = 0
                    # MyAIsOut 객체 생성
        my_ais = schemas.MyAIsOut(
            ai_id=ai_info.ai_id,
            creator_address=ai_info.creator_address,
            created_at=ai_info.created_at,
            ai_name=ai_info.ai_name,
            image_url=ai_info.image_url,
            category=ai_info.category,
            introductions=ai_info.introductions,
            usage=usage  # 계산된 usage 값을 추가
        )

        # my_ais_list에 추가

        my_ais_list.append(my_ais)

    # AIOVerviewList에 담아 반환
    return schemas.MyAIsOutList(ais=my_ais_list)


def get_rags(db: Session, ai_id: str):
    return db.query(models.RAGTable).filter(models.AITable.ai_id == ai_id).all()

def check_ai_exists(db: Session, ai_id: str):
    res =  db.query(models.AITable).filter(models.AITable.ai_id == ai_id).first()
    if res:
        return True
    else:
        return False

def get_ai_detail(db: Session, ai_id: str) -> schemas.AIDetail:
    # AITable과 RAGTable을 ai_id로 조인
    ai_info = get_ai(db=db, ai_id=ai_id)
    user_info = get_user(db=db, user_address=ai_info.creator_address)
    rag_info = get_raglogs_by_aiid(db=db, ai_id=ai_id)

    # RAGTable 데이터는 모든 레코드에서 logs로 변환합니다
    logs = [schemas.RAGTableBase(**rag.__dict__) for rag in rag_info]

    # AIDetail 스키마로 반환
    ai_detail = schemas.AIDetail(
        ai_id=ai_id,
        creator_address=ai_info.creator_address,
        created_at=ai_info.created_at,
        creator = user_info.nickname,
        ai_name=ai_info.ai_name,
        image_url=ai_info.image_url,
        category=ai_info.category,
        introductions=ai_info.introductions,
        logs=logs  # logs는 RAGTableBase 리스트로 설정
    )
    
    return ai_detail

def get_today_ais(db: Session, user_address:str):
    # Join the tables and fetch the data

    ai_infos = db.query(models.AITable).order_by(models.AITable.created_at.desc()).limit(4).all()

    ai_overview_list = []  # 결과를 담을 리스트

    # 각 ai_info에 대해 처리
    for ai_info in ai_infos:
        # 유저 정보를 가져옴
        creator_info = get_user(db=db, user_address=ai_info.creator_address)
        # 유저가 해당 AI를 좋아하는지 여부를 확인
        like_bool = check_like(db=db, user_address=user_address, ai_id=ai_info.ai_id)

        # AIOverview 객체 생성
        ai_overview = schemas.AIOverview(
            ai_id=ai_info.ai_id,
            creator_address=ai_info.creator_address,
            ai_name=ai_info.ai_name,
            creator=creator_info.nickname,  # 유저 닉네임을 가져옴
            like=like_bool,  # 유저가 AI를 좋아하는지 여부
            image_url= ai_info.image_url,
            category= ai_info.category
        )

        # 리스트에 추가
        ai_overview_list.append(ai_overview)

    # 최종 결과로 AIOVerviewList 반환
    return schemas.AIOVerviewList(ais=ai_overview_list) 
    
def get_category_trend_users(db: Session, offset: int, limit : int, category:str, user_address):
    query = db.query(
        models.AITable,
        func.count(models.ChatTable.daily_user_access).label('daily_user_access_count')
    ).join(
        models.ChatTable, models.AITable.ai_id == models.ChatTable.ai_id
    ).filter(
        models.ChatTable.daily_user_access == True  # daily_user_access가 True인 경우만 필터링
    ).group_by(
        models.AITable.ai_id
    ).order_by(
        func.count(models.ChatTable.daily_user_access).desc()  # daily_user_access가 True인 AI를 기준으로 내림차순 정렬
    )

    # 카테고리가 "all"이 아닌 경우에만 필터 추가
    if category != "all":
        query = query.filter(models.AITable.category == category)

    # 페이지네이션 적용
    res = query.offset(offset).limit(limit - offset).all()

    ai_overview_list = []

    for ai_info, daily_user_access_count in res:
        # 해당 유저가 이 AI를 좋아하는지 여부 확인
        creator_info = get_user(db=db, user_address=ai_info.creator_address)
        like_bool = check_like(db=db, user_address=user_address, ai_id=ai_info.ai_id)
        # AIOverview 객체 생성
        ai_overview = schemas.AIOverview(
            ai_id=ai_info.ai_id,
            creator_address=ai_info.creator_address,
            ai_name=ai_info.ai_name,
            creator=creator_info.nickname,  # 유저 닉네임을 가져옴
            like=like_bool,  # 유저가 AI를 좋아하는지 여부
            image_url= ai_info.image_url,
            category= ai_info.category
        )


        ai_overview_list.append(ai_overview)

    # 최종 결과로 AIOVerviewList 반환
    return schemas.AIOVerviewList(ais=ai_overview_list)

# def search_ai(db: Session, name: str):
#     return db.query(models.AITable).filter(models.AITable.name.like(f"%{name}%")).all()
def search_ai_by_name(db: Session, name: str, user_address : str):
    ai_infos = db.query(models.AITable).filter(models.AITable.ai_name.like(f"%{name}%")).all()
    ai_overview_list = []  # 결과를 담을 리스트
    # 각 ai_info에 대해 처리
    for ai_info in ai_infos:
        # 유저 정보를 가져옴
        creator_info = get_user(db=db, user_address=ai_info.creator_address)
        # 유저가 해당 AI를 좋아하는지 여부를 확인
        like_bool = check_like(db=db, user_address=user_address, ai_id=ai_info.ai_id)

        # AIOverview 객체 생성
        ai_overview = schemas.AIOverview(
            ai_id=ai_info.ai_id,
            creator_address=ai_info.creator_address,
            ai_name=ai_info.ai_name,
            creator=creator_info.nickname,  # 유저 닉네임을 가져옴
            like=like_bool,  # 유저가 AI를 좋아하는지 여부
            image_url= ai_info.image_url,
            category= ai_info.category
        )

        # 리스트에 추가
        ai_overview_list.append(ai_overview)

    # 최종 결과로 AIOVerviewList 반환
    return schemas.AIOVerviewList(ais=ai_overview_list) 
# # AITable CRUD functions
# def get_top_10_ai_by_usage(db: Session):
#     return db.query(models.AITable).order_by(models.AITable.usage.desc()).limit(10).all()

def create_ai(db: Session,ai_id:str, ai: schemas.AITableCreate):
    aiDB = schemas.AITableBase(
        ai_id = ai_id,
        creator_address =  ai.creator_address,
        created_at = datetime.now(),
        ai_name = ai.ai_name,
        image_url = ai.image_url,
        category = ai.category,
        introductions = ai.introductions,
    )

    db_ai = models.AITable(**aiDB.model_dump())
    db.add(db_ai)
    db.commit()
    db.refresh(db_ai)
    return db_ai

def update_ai(db: Session, ai_id: str, ai_update: schemas.AITableUserUpdateInput):
    aiUpdateDB = schemas.AITableUpdate(
        name = ai_update.ai_name,
        image_url = ai_update.image_url,
        category= ai_update.category,  # 카테고리 필드, None이 기본값
        introductions=ai_update.introductions  # 소개 필드, None이 기본값
    )
    
    db_ai = get_ai(db, ai_id)
    if db_ai:
        for key, value in aiUpdateDB.model_dump(exclude_unset=True).items():
            setattr(db_ai, key, value)
        db.commit()
        db.refresh(db_ai)
    return db_ai

# def update_collect_ai(db: Session, aiid: str, ai_update: schemas.AITableCollectUpdate):
#     db_ai = get_ai(db, aiid)
#     if db_ai:
#         for key, value in ai_update.model_dump(exclude_unset=True).items():
#             setattr(db_ai, key, value)
#         db.commit()
#         db.refresh(db_ai)
#     return db_ai

def delete_ai(db: Session, ai_id: str):
    db_ai = get_ai(db, ai_id)
    if db_ai:
        db.delete(db_ai)
        db.commit()
    return db_ai

# # AILogTable CRUD functions
# def get_ailog(db: Session, log_id: str):
#     return db.query(models.AILogTable).filter(models.AILogTable.id == log_id).first()

# # RAGTable CRUD functions
def get_raglogs_by_aiid(db: Session, ai_id: str):
    return db.query(models.RAGTable).filter(models.RAGTable.ai_id == ai_id).all()

# def create_rag(db: Session, ai_update: schemas.AITableUserUpdateInput, digest: str, faiss_id: str):
def create_rag(db: Session, ai_id: str, comments: str, digest: str, faiss_id: str):
    rag = schemas.RAGTableCreate(
        ai_id = ai_id,
        created_at = datetime.now(),
        comments = comments,
        tx_url= digest,
        faissid = faiss_id
    )
    db_rag = models.RAGTable(**rag.model_dump())
    db.add(db_rag)
    db.commit()
    db.refresh(db_rag)
    return db_rag

# def update_ailog(db: Session, log_id: str, ailog_update: schemas.AILogTableCreate):
#     db_ailog = get_ailog(db, log_id)
#     if db_ailog:
#         for key, value in ailog_update.model_dump(exclude_unset=True).items():
#             setattr(db_ailog, key, value)
#         db.commit()
#         db.refresh(db_ailog)
#     return db_ailog

# def delete_ailog(db: Session, log_id: str):
#     db_ailog = get_ailog(db, log_id)
#     if db_ailog:
#         db.delete(db_ailog)
#         db.commit()
#     return db_ailog

def delete_raglogs(db: Session, ai_id: str):
    # AI ID와 관련된 모든 로그를 가져옴
    ailogs = get_raglogs_by_aiid(db, ai_id)

    if not ailogs:
        return None  # 로그가 없으면 None 반환

    # 각 로그를 순회하며 삭제
    for log in ailogs:
        db.delete(log)

    # 모든 로그를 삭제한 후 commit
    db.commit()

    return ailogs  # 삭제된 로그 목록 반환