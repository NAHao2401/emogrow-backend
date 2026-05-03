from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class EmotionCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    color_code: Optional[str] = Field(default=None, max_length=20)
    emoji: Optional[str] = Field(default=None, max_length=20)
    audio_url: Optional[str] = None
    animation_url: Optional[str] = None


class EmotionUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = None
    color_code: Optional[str] = Field(default=None, max_length=20)
    emoji: Optional[str] = Field(default=None, max_length=20)
    audio_url: Optional[str] = None
    animation_url: Optional[str] = None


class EmotionResponse(BaseModel):
    emotion_id: int
    name: str
    description: Optional[str] = None
    color_code: Optional[str] = None
    emoji: Optional[str] = None
    audio_url: Optional[str] = None
    animation_url: Optional[str] = None

    class Config:
        from_attributes = True


class EmotionFlashcardCreateRequest(BaseModel):
    emotion_id: int

    title: str = Field(..., min_length=1, max_length=150)

    front_text: str = Field(..., min_length=1, max_length=255)
    front_instruction: Optional[str] = Field(default="Chạm để lật", max_length=255)

    back_title: Optional[str] = Field(default=None, max_length=150)
    back_description: Optional[str] = None

    explanation: Optional[str] = None
    example_situation: Optional[str] = None

    audio_url: Optional[str] = None

    difficulty_level: int = Field(default=1, ge=1, le=5)
    is_active: bool = True


class EmotionFlashcardUpdateRequest(BaseModel):
    emotion_id: Optional[int] = None

    title: Optional[str] = Field(default=None, min_length=1, max_length=150)

    front_text: Optional[str] = Field(default=None, min_length=1, max_length=255)
    front_instruction: Optional[str] = Field(default=None, max_length=255)

    back_title: Optional[str] = Field(default=None, max_length=150)
    back_description: Optional[str] = None

    explanation: Optional[str] = None
    example_situation: Optional[str] = None

    audio_url: Optional[str] = None

    difficulty_level: Optional[int] = Field(default=None, ge=1, le=5)
    is_active: Optional[bool] = None


class EmotionFlashcardResponse(BaseModel):
    flashcard_id: int
    emotion_id: int

    title: str

    front_text: str
    front_instruction: Optional[str] = None

    back_title: Optional[str] = None
    back_description: Optional[str] = None

    explanation: Optional[str] = None
    example_situation: Optional[str] = None

    audio_url: Optional[str] = None

    difficulty_level: int
    is_active: bool

    emotion: Optional[EmotionResponse] = None

    class Config:
        from_attributes = True


class ChildFlashcardProgressResponse(BaseModel):
    progress_id: int
    child_id: int
    flashcard_id: int

    viewed_count: int
    flip_count: int
    explanation_viewed_count: int

    is_completed: bool
    completed_at: Optional[datetime] = None
    last_viewed_at: Optional[datetime] = None

    flashcard: Optional[EmotionFlashcardResponse] = None

    class Config:
        from_attributes = True


class FlashcardInteractionRequest(BaseModel):
    child_id: int
    flashcard_id: int


class ChildFlashcardLearningResponse(BaseModel):
    flashcard: EmotionFlashcardResponse
    progress: Optional[ChildFlashcardProgressResponse] = None