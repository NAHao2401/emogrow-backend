from sqlalchemy.orm import Session
from app.models.emotion import Emotion


def get_all_emotions(db: Session):
    return db.query(Emotion).order_by(Emotion.emotion_id.asc()).all()
