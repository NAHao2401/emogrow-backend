from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.models.child import Child
from app.models.review import EmotionLog, StickerCollection
from app.models.user import User
from app.schemas.review import (
    EmotionLogCreateRequest,
    StickerCollectionCreateRequest,
    EmotionStatisticsResponse,
    EmotionDistributionItem,
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