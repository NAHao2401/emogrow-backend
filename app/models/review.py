from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class EmotionLog(Base):
    __tablename__ = "emotion_logs"

    emotion_log_id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.child_id"), nullable=False)
    emotion_type = Column(String(50), nullable=False, index=True)
    intensity = Column(Integer, nullable=False)
    audio_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    child = relationship("Child", back_populates="emotion_logs")


class StickerCollection(Base):
    __tablename__ = "sticker_collections"

    collection_id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.child_id"), nullable=False)
    sticker_name = Column(String(100), nullable=False)
    note = Column(String(500), nullable=True)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())

    child = relationship("Child", back_populates="sticker_collections")