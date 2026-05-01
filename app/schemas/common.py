from typing import Any, Optional
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[Any] = None


class MessageResponse(BaseModel):
    success: bool = True
    message: str