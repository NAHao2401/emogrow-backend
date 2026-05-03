from pydantic import BaseModel
from typing import Optional


class EmotionResponse(BaseModel):
    emotion_id: int
    name: str
    emoji: Optional[str] = None
    color_code: Optional[str] = None

    class Config:
        from_attributes = True
