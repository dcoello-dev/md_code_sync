from pydantic import BaseModel,  Field
from typing import Optional

class User(BaseModel):
    id: int
    name: str = Field(..., min_length=2)
    email: str
    is_active: bool = True
    bio: Optional[str] = None
