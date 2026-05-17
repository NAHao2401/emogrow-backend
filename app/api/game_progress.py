from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.game_progress import (
    GameProgressResponse,
    UpdateGameProgressRequest,
)
from app.services.game_progress_service import (
    get_child_game_progress,
    update_game_progress,
)

router = APIRouter(prefix="/children", tags=["Game Progress"])


@router.get("/{child_id}/game-progress", response_model=GameProgressResponse)
def get_child_progress(
    child_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_child_game_progress(child_id, db, current_user)


@router.post("/{child_id}/game-progress/complete", response_model=GameProgressResponse)
def complete_level(
    child_id: int,
    data: UpdateGameProgressRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_game_progress(child_id, data, db, current_user)