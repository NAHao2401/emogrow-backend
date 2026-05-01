from fastapi import status


class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: str = "APP_ERROR",
        details=None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details


class BadRequestException(AppException):
    def __init__(self, message: str, error_code: str = "BAD_REQUEST", details=None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, error_code, details)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Không có quyền truy cập", error_code: str = "UNAUTHORIZED", details=None):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, error_code, details)


class NotFoundException(AppException):
    def __init__(self, message: str, error_code: str = "NOT_FOUND", details=None):
        super().__init__(message, status.HTTP_404_NOT_FOUND, error_code, details)


class ConflictException(AppException):
    def __init__(self, message: str, error_code: str = "CONFLICT", details=None):
        super().__init__(message, status.HTTP_409_CONFLICT, error_code, details)