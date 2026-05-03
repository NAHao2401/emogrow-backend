from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel


class CreateDiaryRequest(BaseModel):
    emotion_name: str
    emotion_emoji: Optional[str] = None
    plant_state: str
    feeling_note: Optional[str] = None
    seed_color: Optional[str] = None


class EmotionNested(BaseModel):
    emotion_id: int
    name: str
    emoji: Optional[str] = None
    color_code: Optional[str] = None

    class Config:
        from_attributes = True


class DiaryResponse(BaseModel):
    diary_id: int
    child_id: int
    emotion_id: Optional[int] = None
    diary_date: date
    seed_color: Optional[str] = None
    emotion_name: Optional[str] = None
    emotion_emoji: Optional[str] = None
    plant_state: str
    feeling_note: Optional[str] = None
    voice_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DiaryListItem(BaseModel):
    diary_id: int
    child_id: int
    emotion_id: Optional[int] = None
    emotion_name: Optional[str] = None
    emotion_emoji: Optional[str] = None
    emotion_color: Optional[str] = None
    plant_state: str
    feeling_note: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
