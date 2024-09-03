from sqlalchemy.orm import Session

# 기존에 생성한 모델과 스키마 불러오기
from DB import models, schemas


# 데이터 읽기 - Address로 사용자 불러오기
def get_user(db: Session, user_id: str):
    return db.query(models.Profile).filter(models.Profile.user_name == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Profile).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.ProfileCreate):
    # SQLAlchemy 모델 인스턴스 만들기
    db_user = models.Profile(
        user_name=user.user_name,
        name=user.name,
        sex=user.sex,
        birth=user.birth,
        mbti=user.mbti,
        keywords=user.keywords,
        contents=user.contents
    )
    db.add(db_user)  # DB에 해당 인스턴스 추가하기
    db.commit()  # DB의 변경 사항 저장하기
    db.refresh(db_user)  # 생성된 ID와 같은 DB의 새 데이터를 포함하도록 새로고침
    return db_user

# 데이터 읽기 - 여러 항목 읽어오기
def get_diaries(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.DiaryModel).filter(models.DiaryModel.user_name == user_id).offset(skip).limit(limit).all()


def update_profile(db: Session, user_name: str, updated_data: schemas.ProfileCreate):
    db_user = get_user(db, user_name)
    if not db_user:
        return None
    for key, value in updated_data.model_dump().items():
        if value is not None:
            setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user