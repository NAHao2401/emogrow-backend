from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.child import ChildCreateRequest, ChildUpdateRequest, ChildResponse
from app.schemas.common import MessageResponse
from app.services.child_service import (
    create_child_profile,
    get_my_children,
    get_child_by_id,
    update_child_profile,
    delete_child_profile
)

router = APIRouter(prefix="/children", tags=["Children"])


@router.post("", response_model=ChildResponse)
def create_child(
    data: ChildCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_child_profile(data, db, current_user)


@router.get("/me", response_model=List[ChildResponse])
def get_children(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_my_children(db, current_user)


@router.get("/{child_id}", response_model=ChildResponse)
def get_child(
    child_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_child_by_id(child_id, db, current_user)


@router.put("/{child_id}", response_model=ChildResponse)
def update_child(
    child_id: int,
    data: ChildUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_child_profile(child_id, data, db, current_user)


@router.delete("/{child_id}", response_model=MessageResponse)
def delete_child(
    child_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_child_profile(child_id, db, current_user)