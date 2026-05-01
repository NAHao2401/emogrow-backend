from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictException, UnauthorizedException
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse


def register_user(data: RegisterRequest, db: Session):
    existing_user = db.query(User).filter(User.email == data.email).first()

    if existing_user:
        raise ConflictException(
            message="Email đã được đăng ký",
            error_code="EMAIL_ALREADY_EXISTS"
        )

    new_user = User(
        full_name=data.full_name.strip(),
        email=data.email.lower(),
        password_hash=hash_password(data.password),
        role="parent"
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except SQLAlchemyError:
        db.rollback()
        raise


def login_user(data: LoginRequest, db: Session):
    user = db.query(User).filter(User.email == data.email.lower()).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise UnauthorizedException(
            message="Email hoặc mật khẩu không đúng",
            error_code="INVALID_CREDENTIALS"
        )

    access_token = create_access_token(
        data={
            "sub": str(user.user_id),
            "email": user.email,
            "role": user.role
        }
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user
    )