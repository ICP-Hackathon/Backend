from pydantic import BaseModel
from typing import List, Optional
from datetime import time, datetime
from Schema import base_schemas

class LikeCreate(BaseModel):
    user_address: str
    ai_id: str