from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestException, NotFoundException
from app.models.child import Child
from app.models.user import User
from app.schemas.child import ChildCreateRequest, ChildUpdateRequest


def validate_child_age(age: int):
    if age < 0 or age > 18:
        raise BadRequestException(
            message="Tuổi của trẻ phải nằm trong khoảng 0 đến 18",
            error_code="INVALID_CHILD_AGE"
        )


def create_child_profile(
    data: ChildCreateRequest,
    db: Session,
    current_user: User
):
    validate_child_age(data.age)

    new_child = Child(
        user_id=current_user.user_id,
        nickname=data.nickname.strip(),
        age=data.age,
        avatar_url=data.avatar_url,
        accessibility_needs=data.accessibility_needs
    )

    try:
        db.add(new_child)
        db.commit()
        db.refresh(new_child)
        return new_child

    except SQLAlchemyError:
        db.rollback()
        raise


def get_my_children(
    db: Session,
    current_user: User
):
    return db.query(Child).filter(
        Child.user_id == current_user.user_id
    ).all()


def get_child_by_id(
    child_id: int,
    db: Session,
    current_user: User
):
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


def update_child_profile(
    child_id: int,
    data: ChildUpdateRequest,
    db: Session,
    current_user: User
):
    child = get_child_by_id(child_id, db, current_user)

    if data.age is not None:
        validate_child_age(data.age)

    if data.nickname is not None:
        child.nickname = data.nickname.strip()

    if data.age is not None:
        child.age = data.age

    if data.avatar_url is not None:
        child.avatar_url = data.avatar_url

    if data.accessibility_needs is not None:
        child.accessibility_needs = data.accessibility_needs

    try:
        db.commit()
        db.refresh(child)
        return child

    except SQLAlchemyError:
        db.rollback()
        raise


def delete_child_profile(
    child_id: int,
    db: Session,
    current_user: User
):
    child = get_child_by_id(child_id, db, current_user)

    try:
        db.delete(child)
        db.commit()

        return {
            "success": True,
            "message": "Xóa hồ sơ trẻ thành công"
        }

    except SQLAlchemyError:
        db.rollback()
        raise