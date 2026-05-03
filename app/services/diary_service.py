from datetime import date
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.exceptions import NotFoundException, BadRequestException
from app.models.emotion_diary import EmotionDiary
from app.models.emotion_jar import EmotionJar
from app.models.emotion_jar_item import EmotionJarItem
from app.models.knowledge_bookshelf_item import KnowledgeBookshelfItem
from app.services.child_service import get_child_by_id


def create_diary(child_id: int, data, db: Session, current_user):
    # Ensure child belongs to current user
    child = get_child_by_id(child_id, db, current_user)

    # store emotion name and emoji directly
    new_diary = EmotionDiary(
        child_id=child.child_id,
        emotion_id=None,
        emotion_name=(data.emotion_name.strip() if getattr(data, "emotion_name", None) else None),
        emotion_emoji=getattr(data, "emotion_emoji", None),
        diary_date=date.today(),
        seed_color=data.seed_color,
        plant_state=data.plant_state,
        feeling_note=data.feeling_note,
    )

    try:
        db.add(new_diary)
        db.commit()
        db.refresh(new_diary)

        # If the plant reached 'flower', create a jar item and bookshelf item
        if str(new_diary.plant_state).lower() == "flower":
            # get or create a jar for the child
            jar = db.query(EmotionJar).filter(EmotionJar.child_id == child.child_id).first()

            if jar is None:
                jar = EmotionJar(child_id=child.child_id, name="Main Jar")
                db.add(jar)
                db.commit()
                db.refresh(jar)

            # determine display order
            max_order = db.query(func.coalesce(func.max(EmotionJarItem.display_order), 0)).filter(
                EmotionJarItem.jar_id == jar.jar_id
            ).scalar() or 0

            jar_item = EmotionJarItem(
                jar_id=jar.jar_id,
                diary_id=new_diary.diary_id,
                emotion_id=new_diary.emotion_id,
                item_date=new_diary.diary_date,
                color_code=(new_diary.seed_color),
                display_order=(max_order + 1)
            )

            db.add(jar_item)
            db.commit()
            db.refresh(jar_item)

            # create a bookshelf item as a short knowledge preview
            note_preview = (new_diary.feeling_note or "")[:300]

            book_item = KnowledgeBookshelfItem(
                child_id=child.child_id,
                diary_id=new_diary.diary_id,
                emotion_id=new_diary.emotion_id,
                title=f"{new_diary.emotion_name or 'Cảm xúc'} - Câu chuyện",
                cover_image_url=None,
                note_preview=note_preview
            )

            db.add(book_item)
            db.commit()
            db.refresh(book_item)

        # Build response matching frontend expectation
        return {
            "diary_id": new_diary.diary_id,
            "child_id": new_diary.child_id,
            "emotion_id": new_diary.emotion_id,
            "emotion_name": new_diary.emotion_name,
            "emotion_emoji": new_diary.emotion_emoji,
            "emotion_color": None,
            "plant_state": new_diary.plant_state,
            "feeling_note": new_diary.feeling_note,
            "created_at": new_diary.created_at,
        }

    except SQLAlchemyError:
        db.rollback()
        raise


def get_diaries(child_id: int, db: Session, current_user):
    # Verify ownership
    get_child_by_id(child_id, db, current_user)

    diaries = db.query(EmotionDiary).filter(
        EmotionDiary.child_id == child_id
    ).order_by(EmotionDiary.created_at.desc()).all()

    results = []
    for diary in diaries:
        results.append({
            "diary_id": diary.diary_id,
            "child_id": diary.child_id,
            "emotion_id": diary.emotion_id,
            "emotion_name": diary.emotion_name,
            "emotion_emoji": diary.emotion_emoji,
            "emotion_color": None,
            "plant_state": diary.plant_state,
            "feeling_note": diary.feeling_note,
            "created_at": diary.created_at,
        })

    return results
