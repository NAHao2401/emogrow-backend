from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class EmotionDiary(Base):
    __tablename__ = "emotion_diaries"

    diary_id = Column(Integer, primary_key=True, index=True)

    child_id = Column(Integer, ForeignKey("children.child_id"), nullable=False)
    # keep optional emotion_id for compatibility, but allow direct text storage
    emotion_id = Column(Integer, ForeignKey("emotions.emotion_id"), nullable=True)
    emotion_name = Column(String(100), nullable=True)
    emotion_emoji = Column(String(10), nullable=True)

    diary_date = Column(Date, nullable=False, server_default=func.current_date())
    seed_color = Column(String(20), nullable=True)
    plant_state = Column(String(50), nullable=False)
    feeling_note = Column(Text, nullable=True)
    voice_url = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    child = relationship("Child")
