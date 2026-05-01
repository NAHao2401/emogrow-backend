from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Child(Base):
    __tablename__ = "children"

    child_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    nickname = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    avatar_url = Column(String(255), nullable=True)
    accessibility_needs = Column(String(500), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    parent = relationship("User")