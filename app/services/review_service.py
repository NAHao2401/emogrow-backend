from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.models.child import Child
from app.models.review import EmotionLog, StickerCollection, ChildReadBook
from app.models.user import User
from app.schemas.review import (
    EmotionLogCreateRequest,
    StickerCollectionCreateRequest,
    EmotionStatisticsResponse,
    EmotionDistributionItem,
    EmotionLogResponse,
    StickerCollectionResponse,
    ProgressResponse,
    BookReadResponse
)


def get_child_for_user(
    child_id: int,
    db: Session,
    current_user: User,
):
    child = db.query(Child).filter(
        Child.child_id == child_id,
        Child.user_id == current_user.user_id,
    ).first()

    if child is None:
        raise NotFoundException(
            message="Không tìm thấy hồ sơ trẻ",
            error_code="CHILD_NOT_FOUND"
        )

    return child


def create_emotion_log(
    data: EmotionLogCreateRequest,
    db: Session,
    current_user: User,
):
    get_child_for_user(data.child_id, db, current_user)

    emotion_log = EmotionLog(
        child_id=data.child_id,
        emotion_type=data.emotion_type.strip(),
        intensity=data.intensity,
        source=data.source,
        note=data.note,
        audio_url=data.audio_url,
    )

    db.add(emotion_log)
    db.commit()
    db.refresh(emotion_log)
    return emotion_log


def create_sticker(
    data: StickerCollectionCreateRequest,
    db: Session,
    current_user: User,
):
    get_child_for_user(data.child_id, db, current_user)

    sticker = StickerCollection(
        child_id=data.child_id,
        sticker_name=data.sticker_name.strip(),
        note=data.note,
    )

    db.add(sticker)
    db.commit()
    db.refresh(sticker)
    return sticker


def get_emotion_statistics(
    child_id: int,
    db: Session,
    current_user: User,
):
    get_child_for_user(child_id, db, current_user)

    distribution_rows = db.query(
        EmotionLog.emotion_type,
        func.count(EmotionLog.emotion_log_id).label("count")
    ).filter(
        EmotionLog.child_id == child_id
    ).group_by(
        EmotionLog.emotion_type
    ).all()

    totals = db.query(
        func.count(EmotionLog.emotion_log_id).label("total_count"),
        func.avg(EmotionLog.intensity).label("average_intensity")
    ).filter(
        EmotionLog.child_id == child_id
    ).first()

    distribution = [
        EmotionDistributionItem(
            emotion_type=row.emotion_type,
            count=row.count,
        )
        for row in distribution_rows
    ]

    return EmotionStatisticsResponse(
        child_id=child_id,
        total_count=totals.total_count or 0,
        average_intensity=round(float(totals.average_intensity or 0), 2),
        distribution=distribution,
    )


def get_emotion_logs(
    child_id: int,
    db: Session,
    current_user: User,
):
    get_child_for_user(child_id, db, current_user)
    logs = db.query(EmotionLog).filter(EmotionLog.child_id == child_id).all()

    return [
        EmotionLogResponse(
            emotion_log_id=log.emotion_log_id,
            child_id=log.child_id,
            emotion_type=log.emotion_type,
            intensity=log.intensity,
            source=log.source,
            note=log.note,
            audio_url=log.audio_url,
            created_at=log.created_at.isoformat() if log.created_at else ""
        )
        for log in logs
    ]


def get_stickers(
    child_id: int,
    db: Session,
    current_user: User,
):
    get_child_for_user(child_id, db, current_user)
    stickers = db.query(StickerCollection).filter(StickerCollection.child_id == child_id).all()

    return [
        StickerCollectionResponse(
            collection_id=s.collection_id,
            child_id=s.child_id,
            sticker_name=s.sticker_name,
            note=s.note,
            earned_at=s.earned_at.isoformat() if s.earned_at else ""
        )
        for s in stickers
    ]


def mark_book_as_read(
    child_id: int,
    book_id: str,
    db: Session,
    current_user: User,
):
    get_child_for_user(child_id, db, current_user)

    existing = db.query(ChildReadBook).filter(
        ChildReadBook.child_id == child_id,
        ChildReadBook.book_id == book_id
    ).first()

    if existing:
        return existing

    record = ChildReadBook(child_id=child_id, book_id=book_id)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_progress(
    child_id: int,
    db: Session,
    current_user: User,
):
    get_child_for_user(child_id, db, current_user)

    books = db.query(ChildReadBook).filter(ChildReadBook.child_id == child_id).all()
    stickers = db.query(StickerCollection).filter(StickerCollection.child_id == child_id).all()

    return ProgressResponse(
        read_book_ids=[b.book_id for b in books],
        unlocked_sticker_ids=[s.sticker_name for s in stickers]
    )
