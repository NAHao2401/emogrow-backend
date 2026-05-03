from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.diary import CreateDiaryRequest, DiaryListItem
from app.services.diary_service import create_diary, get_diaries

router = APIRouter(prefix="/api", tags=["Journal"])





@router.post("/children/{child_id}/diaries", response_model=DiaryListItem)
def post_diary(
    child_id: int,
    data: CreateDiaryRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_diary(child_id, data, db, current_user)


@router.get("/children/{child_id}/diaries", response_model=List[DiaryListItem])
def list_diaries(
    child_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_diaries(child_id, db, current_user)
