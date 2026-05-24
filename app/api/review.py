from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.review import (
    EmotionStatisticsResponse,
    EmotionLogResponse,
    StickerCollectionResponse,
    EmotionLogCreateRequest,
    BookReadResponse,
    ProgressResponse,
)
from app.services.review_service import (
    get_emotion_statistics,
    get_emotion_logs,
    get_stickers,
    create_emotion_log,
    mark_book_as_read,
    get_progress,
)

router = APIRouter(prefix="/review", tags=["Review"])


@router.get("/children/{child_id}/emotion-statistics", response_model=EmotionStatisticsResponse)
def read_emotion_statistics(
    child_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_emotion_statistics(child_id, db, current_user)


@router.post("/children/{child_id}/logs", response_model=EmotionLogResponse)
def post_emotion_log(
    child_id: int,
    data: EmotionLogCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data.child_id = child_id
    return create_emotion_log(data, db, current_user)


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


@router.post("/children/{child_id}/books/{book_id}/read", response_model=BookReadResponse)
def post_book_read(
    child_id: int,
    book_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return mark_book_as_read(child_id, book_id, db, current_user)


@router.get("/children/{child_id}/progress", response_model=ProgressResponse)
def read_progress(
    child_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_progress(child_id, db, current_user)
