from typing import Optional
from pydantic import BaseModel, Field


class ChildCreateRequest(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=18)
    avatar_url: Optional[str] = None
    accessibility_needs: Optional[str] = Field(default=None, max_length=500)


class ChildUpdateRequest(BaseModel):
    nickname: Optional[str] = Field(default=None, min_length=1, max_length=100)
    age: Optional[int] = Field(default=None, ge=0, le=18)
    avatar_url: Optional[str] = None
    accessibility_needs: Optional[str] = Field(default=None, max_length=500)


class ChildResponse(BaseModel):
    child_id: int
    user_id: int
    nickname: str
    age: int
    avatar_url: Optional[str] = None
    accessibility_needs: Optional[str] = None

    class Config:
        from_attributes = True