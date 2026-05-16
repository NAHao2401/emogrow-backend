from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class EmotionBase(BaseModel):
    name: str
    description: Optional[str] = None
    color_code: Optional[str] = None
    emoji: Optional[str] = None
    audio_url: Optional[str] = None
    animation_url: Optional[str] = None

class EmotionResponse(EmotionBase):
    emotion_id: int

    class Config:
        from_attributes = True

class EmotionFlashcardBase(BaseModel):
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

class EmotionFlashcardResponse(EmotionFlashcardBase):
    flashcard_id: int
    emotion: Optional[EmotionResponse] = None

    class Config:
        from_attributes = True

class ChildFlashcardProgressBase(BaseModel):
    child_id: int
    flashcard_id: int
    viewed_count: int
    flip_count: int
    explanation_viewed_count: int
    is_completed: bool
    completed_at: Optional[str] = None
    last_viewed_at: Optional[str] = None

class ChildFlashcardProgressResponse(ChildFlashcardProgressBase):
    progress_id: int
    flashcard: Optional[EmotionFlashcardResponse] = None

    class Config:
        from_attributes = True

class FlashcardInteractionRequest(BaseModel):
    child_id: int
    flashcard_id: int

class ChildFlashcardLearningResponse(BaseModel):
    flashcard: EmotionFlashcardResponse
    progress: Optional[ChildFlashcardProgressResponse] = None
