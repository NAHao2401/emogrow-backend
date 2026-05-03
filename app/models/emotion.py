from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Emotion(Base):
    __tablename__ = "emotions"

    emotion_id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    color_code = Column(String(20), nullable=True)
    emoji = Column(String(20), nullable=True)

    audio_url = Column(String(255), nullable=True)
    animation_url = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    flashcards = relationship(
        "EmotionFlashcard",
        back_populates="emotion",
        cascade="all, delete-orphan"
    )


class EmotionFlashcard(Base):
    __tablename__ = "emotion_flashcards"

    flashcard_id = Column(Integer, primary_key=True, index=True)
    emotion_id = Column(
        Integer,
        ForeignKey("emotions.emotion_id"),
        nullable=False
    )

    title = Column(String(150), nullable=False)

    front_text = Column(String(255), nullable=False)
    front_instruction = Column(String(255), nullable=True)

    back_title = Column(String(150), nullable=True)
    back_description = Column(Text, nullable=True)

    explanation = Column(Text, nullable=True)
    example_situation = Column(Text, nullable=True)

    audio_url = Column(String(255), nullable=True)

    difficulty_level = Column(Integer, default=1, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    emotion = relationship(
        "Emotion",
        back_populates="flashcards"
    )

    progresses = relationship(
        "ChildFlashcardProgress",
        back_populates="flashcard",
        cascade="all, delete-orphan"
    )


class ChildFlashcardProgress(Base):
    __tablename__ = "child_flashcard_progress"

    progress_id = Column(Integer, primary_key=True, index=True)

    child_id = Column(
        Integer,
        ForeignKey("children.child_id"),
        nullable=False
    )

    flashcard_id = Column(
        Integer,
        ForeignKey("emotion_flashcards.flashcard_id"),
        nullable=False
    )

    viewed_count = Column(Integer, default=0, nullable=False)
    flip_count = Column(Integer, default=0, nullable=False)
    explanation_viewed_count = Column(Integer, default=0, nullable=False)

    is_completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    last_viewed_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    flashcard = relationship(
        "EmotionFlashcard",
        back_populates="progresses"
    )

    child = relationship("Child")

    __table_args__ = (
        UniqueConstraint(
            "child_id",
            "flashcard_id",
            name="uq_child_flashcard_progress"
        ),
    )