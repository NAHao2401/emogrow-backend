from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EmotionResponse(BaseModel):
    emotion_id: int
    name: str
    description: Optional[str] = None
    color_code: Optional[str] = None
    emoji: Optional[str] = None
    audio_url: Optional[str] = None
    animation_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
