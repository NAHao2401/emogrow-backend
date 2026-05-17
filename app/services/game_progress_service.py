from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.game_progress import GameProgress
from app.models.user import User
from app.schemas.game_progress import UpdateGameProgressRequest
from app.services.child_service import get_child_by_id


def get_or_create_game_progress(
    child_id: int,
    db: Session,
    current_user: User
):
    get_child_by_id(child_id, db, current_user)

    progress = db.query(GameProgress).filter(
        GameProgress.child_id == child_id
    ).first()

    if progress is None:
        progress = GameProgress(
            child_id=child_id,
            last_passed_level=0
        )
        db.add(progress)
        db.flush()

    return progress


def update_game_progress(
    child_id: int,
    data: UpdateGameProgressRequest,
    db: Session,
    current_user: User
):
    progress = get_or_create_game_progress(child_id, db, current_user)
    progress.last_passed_level = max(progress.last_passed_level, data.last_passed_level)

    try:
        db.commit()
        db.refresh(progress)
        return progress

    except SQLAlchemyError:
        db.rollback()
        raise


def get_child_game_progress(
    child_id: int,
    db: Session,
    current_user: User
):
    get_child_by_id(child_id, db, current_user)

    progress = db.query(GameProgress).filter(
        GameProgress.child_id == child_id
    ).first()

    if progress is None:
        progress = GameProgress(
            child_id=child_id,
            last_passed_level=0
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)

    return progress