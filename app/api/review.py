from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.review import (
    EmotionStatisticsResponse,
    EmotionLogResponse,
    StickerCollectionResponse
)
from app.services.review_service import (
    get_emotion_statistics,
    get_emotion_logs,
    get_stickers
)

router = APIRouter(prefix="/review", tags=["Review"])


@router.get("/children/{child_id}/emotion-statistics", response_model=EmotionStatisticsResponse)
def read_emotion_statistics(
    child_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_emotion_statistics(child_id, db, current_user)


@router.get("/children/{child_id}/logs", response_model=List[EmotionLogResponse])
def read_emotion_logs(
    child_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_emotion_logs(child_id, db, current_user)


@router.get("/children/{child_id}/stickers", response_model=List[StickerCollectionResponse])
def read_stickers(
    child_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_stickers(child_id, db, current_user)