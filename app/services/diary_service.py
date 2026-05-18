from datetime import date
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.core.exceptions import NotFoundException, BadRequestException
from app.models.emotion import Emotion
from app.models.emotion_diary import EmotionDiary
from app.services.child_service import get_child_by_id


def create_diary(child_id: int, data, db: Session, current_user):
    # Ensure child belongs to current user
    child = get_child_by_id(child_id, db, current_user)

    # Verify emotion exists
    emotion = db.query(Emotion).filter(Emotion.emotion_id == data.emotion_id).first()
    if not emotion:
        raise NotFoundException(message="Không tìm thấy cảm xúc", error_code="EMOTION_NOT_FOUND")

    new_diary = EmotionDiary(
        child_id=child.child_id,
        emotion_id=data.emotion_id,
        diary_date=data.diary_date,
        seed_color=data.seed_color,
        plant_state=data.plant_state,
        feeling_note=data.feeling_note,
        voice_url=data.voice_url,
    )

    try:
        db.add(new_diary)
        db.commit()
        db.refresh(new_diary)

        # Build response matching frontend expectation
        return {
            "diary_id": new_diary.diary_id,
            "child_id": new_diary.child_id,
            "emotion_id": new_diary.emotion_id,
            "emotion_name": emotion.name,
            "emotion_emoji": emotion.emoji,
            "diary_date": new_diary.diary_date,
            "seed_color": new_diary.seed_color,
            "plant_state": new_diary.plant_state,
            "feeling_note": new_diary.feeling_note,
            "voice_url": new_diary.voice_url,
            "created_at": new_diary.created_at,
        }

    except SQLAlchemyError:
        db.rollback()
        raise


def get_diaries(child_id: int, db: Session, current_user, date_filter: date = None):
    # Verify ownership
    get_child_by_id(child_id, db, current_user)

    query = db.query(EmotionDiary).options(joinedload(EmotionDiary.emotion)).filter(EmotionDiary.child_id == child_id)
    
    if date_filter:
        query = query.filter(EmotionDiary.diary_date == date_filter)

    diaries = query.order_by(EmotionDiary.created_at.desc()).all()

    results = []
    for diary in diaries:
        results.append({
            "diary_id": diary.diary_id,
            "child_id": diary.child_id,
            "emotion_id": diary.emotion_id,
            "emotion_name": diary.emotion.name if diary.emotion else diary.emotion_name,
            "emotion_emoji": diary.emotion.emoji if diary.emotion else diary.emotion_emoji,
            "diary_date": diary.diary_date,
            "seed_color": diary.seed_color,
            "plant_state": diary.plant_state,
            "feeling_note": diary.feeling_note,
            "voice_url": diary.voice_url,
            "created_at": diary.created_at,
        })

    return results
