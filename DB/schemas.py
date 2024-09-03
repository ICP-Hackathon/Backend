from typing import List, Union
from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


# ProfileBase 생성
class ProfileBase(BaseModel):
    user_name: str
    name: Union[str, None] = None
    sex: Union[str, None] = None
    birth: Union[date, None] = None
    mbti: Union[str, None] = None
    keywords: Union[str, None] = None
    contents: Union[str, None] = None

# ProfileCreate 생성 (ProfileBase 상속)
class ProfileCreate(ProfileBase):
    pass

# API에서 데이터를 읽을 때/반환할 때 사용될 모델
class Profile(ProfileBase):
    class Config:
        orm_mode = True

class DiaryBase(BaseModel):
    date: Optional[datetime] = None  # timestamp 타입을 지원하는 datetime 사용
    keywords: Optional[str] = None
    contents: Optional[str] = None
    happy: Optional[int] = None
    sad: Optional[int] = None
    love: Optional[int] = None
    user_name: str

    class Config:
        orm_mode = True

class DiaryCreate(DiaryBase):
    pass

class DiaryRead(DiaryBase):
    id: int