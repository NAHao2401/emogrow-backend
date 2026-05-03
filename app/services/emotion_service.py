from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import BadRequestException, NotFoundException
from app.models.child import Child
from app.models.emotion import Emotion, EmotionFlashcard, ChildFlashcardProgress
from app.models.user import User
from app.schemas.emotion import (
    EmotionCreateRequest,
    EmotionUpdateRequest,
    EmotionFlashcardCreateRequest,
    EmotionFlashcardUpdateRequest
)


def ensure_admin(current_user: User):
    if current_user.role != "admin":
        raise BadRequestException(
            message="Chỉ admin mới có quyền thực hiện thao tác này",
            error_code="ADMIN_REQUIRED"
        )


def get_child_of_current_user(child_id: int, db: Session, current_user: User):
    child = db.query(Child).filter(
        Child.child_id == child_id,
        Child.user_id == current_user.user_id
    ).first()

    if child is None:
        raise NotFoundException(
            message="Không tìm thấy hồ sơ trẻ",
            error_code="CHILD_NOT_FOUND"
        )

    return child


def get_emotion_or_404(emotion_id: int, db: Session):
    emotion = db.query(Emotion).filter(
        Emotion.emotion_id == emotion_id
    ).first()

    if emotion is None:
        raise NotFoundException(
            message="Không tìm thấy cảm xúc",
            error_code="EMOTION_NOT_FOUND"
        )

    return emotion


def get_flashcard_or_404(flashcard_id: int, db: Session):
    flashcard = db.query(EmotionFlashcard).options(
        joinedload(EmotionFlashcard.emotion)
    ).filter(
        EmotionFlashcard.flashcard_id == flashcard_id
    ).first()

    if flashcard is None:
        raise NotFoundException(
            message="Không tìm thấy thẻ học cảm xúc",
            error_code="FLASHCARD_NOT_FOUND"
        )

    return flashcard


def create_emotion(data: EmotionCreateRequest, db: Session, current_user: User):
    ensure_admin(current_user)

    emotion = Emotion(
        name=data.name.strip(),
        description=data.description,
        color_code=data.color_code,
        emoji=data.emoji,
        audio_url=data.audio_url,
        animation_url=data.animation_url
    )

    try:
        db.add(emotion)
        db.commit()
        db.refresh(emotion)
        return emotion

    except SQLAlchemyError:
        db.rollback()
        raise


def get_all_emotions(db: Session):
    return db.query(Emotion).order_by(Emotion.emotion_id.asc()).all()


def update_emotion(
    emotion_id: int,
    data: EmotionUpdateRequest,
    db: Session,
    current_user: User
):
    ensure_admin(current_user)

    emotion = get_emotion_or_404(emotion_id, db)

    if data.name is not None:
        emotion.name = data.name.strip()

    if data.description is not None:
        emotion.description = data.description

    if data.color_code is not None:
        emotion.color_code = data.color_code

    if data.emoji is not None:
        emotion.emoji = data.emoji

    if data.audio_url is not None:
        emotion.audio_url = data.audio_url

    if data.animation_url is not None:
        emotion.animation_url = data.animation_url

    try:
        db.commit()
        db.refresh(emotion)
        return emotion

    except SQLAlchemyError:
        db.rollback()
        raise


def delete_emotion(emotion_id: int, db: Session, current_user: User):
    ensure_admin(current_user)

    emotion = get_emotion_or_404(emotion_id, db)

    try:
        db.delete(emotion)
        db.commit()

        return {
            "success": True,
            "message": "Xóa cảm xúc thành công"
        }

    except SQLAlchemyError:
        db.rollback()
        raise


def create_flashcard(
    data: EmotionFlashcardCreateRequest,
    db: Session,
    current_user: User
):
    ensure_admin(current_user)

    get_emotion_or_404(data.emotion_id, db)

    flashcard = EmotionFlashcard(
        emotion_id=data.emotion_id,
        title=data.title.strip(),
        front_text=data.front_text.strip(),
        front_instruction=data.front_instruction,
        back_title=data.back_title,
        back_description=data.back_description,
        explanation=data.explanation,
        example_situation=data.example_situation,
        audio_url=data.audio_url,
        difficulty_level=data.difficulty_level,
        is_active=data.is_active
    )

    try:
        db.add(flashcard)
        db.commit()
        db.refresh(flashcard)

        return get_flashcard_or_404(flashcard.flashcard_id, db)

    except SQLAlchemyError:
        db.rollback()
        raise


def get_all_flashcards(db: Session):
    return db.query(EmotionFlashcard).options(
        joinedload(EmotionFlashcard.emotion)
    ).filter(
        EmotionFlashcard.is_active == True
    ).order_by(
        EmotionFlashcard.difficulty_level.asc(),
        EmotionFlashcard.flashcard_id.asc()
    ).all()


def get_flashcards_by_emotion(emotion_id: int, db: Session):
    get_emotion_or_404(emotion_id, db)

    return db.query(EmotionFlashcard).options(
        joinedload(EmotionFlashcard.emotion)
    ).filter(
        EmotionFlashcard.emotion_id == emotion_id,
        EmotionFlashcard.is_active == True
    ).order_by(
        EmotionFlashcard.difficulty_level.asc(),
        EmotionFlashcard.flashcard_id.asc()
    ).all()


def update_flashcard(
    flashcard_id: int,
    data: EmotionFlashcardUpdateRequest,
    db: Session,
    current_user: User
):
    ensure_admin(current_user)

    flashcard = get_flashcard_or_404(flashcard_id, db)

    if data.emotion_id is not None:
        get_emotion_or_404(data.emotion_id, db)
        flashcard.emotion_id = data.emotion_id

    if data.title is not None:
        flashcard.title = data.title.strip()

    if data.front_text is not None:
        flashcard.front_text = data.front_text.strip()

    if data.front_instruction is not None:
        flashcard.front_instruction = data.front_instruction

    if data.back_title is not None:
        flashcard.back_title = data.back_title

    if data.back_description is not None:
        flashcard.back_description = data.back_description

    if data.explanation is not None:
        flashcard.explanation = data.explanation

    if data.example_situation is not None:
        flashcard.example_situation = data.example_situation

    if data.audio_url is not None:
        flashcard.audio_url = data.audio_url

    if data.difficulty_level is not None:
        flashcard.difficulty_level = data.difficulty_level

    if data.is_active is not None:
        flashcard.is_active = data.is_active

    try:
        db.commit()
        db.refresh(flashcard)

        return get_flashcard_or_404(flashcard.flashcard_id, db)

    except SQLAlchemyError:
        db.rollback()
        raise


def delete_flashcard(flashcard_id: int, db: Session, current_user: User):
    ensure_admin(current_user)

    flashcard = get_flashcard_or_404(flashcard_id, db)

    try:
        db.delete(flashcard)
        db.commit()

        return {
            "success": True,
            "message": "Xóa thẻ học cảm xúc thành công"
        }

    except SQLAlchemyError:
        db.rollback()
        raise


def get_or_create_progress(child_id: int, flashcard_id: int, db: Session):
    progress = db.query(ChildFlashcardProgress).filter(
        ChildFlashcardProgress.child_id == child_id,
        ChildFlashcardProgress.flashcard_id == flashcard_id
    ).first()

    if progress is None:
        progress = ChildFlashcardProgress(
            child_id=child_id,
            flashcard_id=flashcard_id,
            viewed_count=0,
            flip_count=0,
            explanation_viewed_count=0,
            is_completed=False
        )

        db.add(progress)
        db.flush()

    return progress


def view_flashcard(child_id: int, flashcard_id: int, db: Session, current_user: User):
    get_child_of_current_user(child_id, db, current_user)
    flashcard = get_flashcard_or_404(flashcard_id, db)

    progress = get_or_create_progress(child_id, flashcard_id, db)
    progress.viewed_count += 1
    progress.last_viewed_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(progress)

        return {
            "flashcard": flashcard,
            "progress": progress
        }

    except SQLAlchemyError:
        db.rollback()
        raise


def flip_flashcard(child_id: int, flashcard_id: int, db: Session, current_user: User):
    get_child_of_current_user(child_id, db, current_user)
    get_flashcard_or_404(flashcard_id, db)

    progress = get_or_create_progress(child_id, flashcard_id, db)
    progress.flip_count += 1
    progress.last_viewed_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(progress)
        return progress

    except SQLAlchemyError:
        db.rollback()
        raise


def view_flashcard_explanation(
    child_id: int,
    flashcard_id: int,
    db: Session,
    current_user: User
):
    get_child_of_current_user(child_id, db, current_user)
    get_flashcard_or_404(flashcard_id, db)

    progress = get_or_create_progress(child_id, flashcard_id, db)
    progress.explanation_viewed_count += 1
    progress.last_viewed_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(progress)
        return progress

    except SQLAlchemyError:
        db.rollback()
        raise


def complete_flashcard(
    child_id: int,
    flashcard_id: int,
    db: Session,
    current_user: User
):
    get_child_of_current_user(child_id, db, current_user)
    get_flashcard_or_404(flashcard_id, db)

    progress = get_or_create_progress(child_id, flashcard_id, db)
    progress.is_completed = True
    progress.completed_at = datetime.now(timezone.utc)
    progress.last_viewed_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(progress)
        return progress

    except SQLAlchemyError:
        db.rollback()
        raise


def get_child_flashcard_progress(
    child_id: int,
    db: Session,
    current_user: User
):
    get_child_of_current_user(child_id, db, current_user)

    return db.query(ChildFlashcardProgress).options(
        joinedload(ChildFlashcardProgress.flashcard).joinedload(
            EmotionFlashcard.emotion
        )
    ).filter(
        ChildFlashcardProgress.child_id == child_id
    ).order_by(
        ChildFlashcardProgress.last_viewed_at.desc()
    ).all()