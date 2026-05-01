from typing import Optional, List
from pydantic import BaseModel, Field


class EmotionLogCreateRequest(BaseModel):
    child_id: int
    emotion_type: str = Field(..., min_length=1, max_length=50)
    intensity: int = Field(..., ge=1, le=10)
    audio_url: Optional[str] = Field(default=None, max_length=500)


class StickerCollectionCreateRequest(BaseModel):
    child_id: int
    sticker_name: str = Field(..., min_length=1, max_length=100)
    note: Optional[str] = Field(default=None, max_length=500)


class EmotionDistributionItem(BaseModel):
    emotion_type: str
    count: int

    class Config:
        from_attributes = True


class EmotionStatisticsResponse(BaseModel):
    child_id: int
    total_count: int
    average_intensity: float
    distribution: List[EmotionDistributionItem]

    class Config:
        from_attributes = True