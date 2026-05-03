from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class EmotionJarItem(Base):
    __tablename__ = "emotion_jar_items"

    jar_item_id = Column(Integer, primary_key=True, index=True)
    jar_id = Column(Integer, ForeignKey("emotion_jars.jar_id"))
    diary_id = Column(Integer, ForeignKey("emotion_diaries.diary_id"))
    emotion_id = Column(Integer, ForeignKey("emotions.emotion_id"))

    item_date = Column(Date, nullable=True)
    color_code = Column(String(20), nullable=True)
    display_order = Column(Integer, nullable=True)

    jar = relationship("EmotionJar", back_populates="items")
    diary = relationship("EmotionDiary")
    emotion = relationship("Emotion")
