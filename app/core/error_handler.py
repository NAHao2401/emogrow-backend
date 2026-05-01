from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import AppException


async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "error_code": exc.error_code,
            "details": exc.details
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []

    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error.get("loc", [])),
            "message": error.get("msg"),
            "type": error.get("type")
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Dữ liệu không hợp lệ",
            "error_code": "VALIDATION_ERROR",
            "details": errors
        }
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Lỗi cơ sở dữ liệu",
            "error_code": "DATABASE_ERROR",
            "details": None
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Đã xảy ra lỗi hệ thống",
            "error_code": "INTERNAL_SERVER_ERROR",
            "details": None
        }
    )