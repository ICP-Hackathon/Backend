from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    user_address: str
    nickname: str = '0.0'
    gender: str
    country: str
    interest: str
    profile_image_url: str

    class Config:
        from_attributes = True

class UserList(BaseModel):
    users : List[User]
    class Config:
        from_attributes = True