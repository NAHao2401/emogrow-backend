from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class KnowledgeBookshelfItem(Base):
    __tablename__ = "knowledge_bookshelf_items"

    book_item_id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.child_id"))
    diary_id = Column(Integer, ForeignKey("emotion_diaries.diary_id"))
    emotion_id = Column(Integer, ForeignKey("emotions.emotion_id"))

    title = Column(String(255), nullable=False)
    cover_image_url = Column(String(255), nullable=True)
    note_preview = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    child = relationship("Child")
    diary = relationship("EmotionDiary")
    emotion = relationship("Emotion")
