from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Emotion(Base):
    __tablename__ = "emotions"

    emotion_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    color_code = Column(String(20), nullable=True)
    emoji = Column(String(10), nullable=True)
    audio_url = Column(String(255), nullable=True)
    animation_url = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
