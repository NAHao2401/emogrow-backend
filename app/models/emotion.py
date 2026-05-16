from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Emotion(Base):
    __tablename__ = "emotions"
    
    emotion_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    color_code = Column(String(50), nullable=True)
    emoji = Column(String(50), nullable=True)
    audio_url = Column(String(500), nullable=True)
    animation_url = Column(String(500), nullable=True)

    flashcards = relationship("EmotionFlashcard", back_populates="emotion")

class EmotionFlashcard(Base):
    __tablename__ = "emotion_flashcards"
    
    flashcard_id = Column(Integer, primary_key=True, index=True)
    emotion_id = Column(Integer, ForeignKey("emotions.emotion_id"), nullable=False)
    
    title = Column(String(200), nullable=False)
    front_text = Column(String(500), nullable=False)
    front_instruction = Column(String(500), nullable=True)
    back_title = Column(String(200), nullable=True)
    back_description = Column(String(1000), nullable=True)
    explanation = Column(String(1000), nullable=True)
    example_situation = Column(String(1000), nullable=True)
    audio_url = Column(String(500), nullable=True)
    difficulty_level = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)

    emotion = relationship("Emotion", back_populates="flashcards")
    progresses = relationship("ChildFlashcardProgress", back_populates="flashcard")

class ChildFlashcardProgress(Base):
    __tablename__ = "child_flashcard_progresses"
    
    progress_id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.child_id"), nullable=False)
    flashcard_id = Column(Integer, ForeignKey("emotion_flashcards.flashcard_id"), nullable=False)

    viewed_count = Column(Integer, default=0)
    flip_count = Column(Integer, default=0)
    explanation_viewed_count = Column(Integer, default=0)

    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    last_viewed_at = Column(DateTime(timezone=True), nullable=True)

    child = relationship("Child", back_populates="flashcard_progresses")
    flashcard = relationship("EmotionFlashcard", back_populates="progresses")
