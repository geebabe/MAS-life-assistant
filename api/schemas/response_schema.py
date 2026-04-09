from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List, Any

T = TypeVar("T")

class BaseResponse(BaseModel, Generic[T]):
    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    errors: Optional[List[dict]] = None
