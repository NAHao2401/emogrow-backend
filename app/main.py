from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.api.auth import router as auth_router
from app.api.children import router as children_router
from app.api.review import router as review_router
from app.core.exceptions import AppException
from app.core.error_handler import (
    app_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler
)
from app.db.base import Base
from app.db.session import engine
from app.models import user, child, review

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EMOGROW Backend API")

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(auth_router)
app.include_router(children_router)
app.include_router(review_router)


@app.get("/")
def root():
    return {"message": "EMOGROW Backend is running"}