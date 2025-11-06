from typing import TypeVar, Generic, Optional, Any
from pydantic import BaseModel

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    """
    统一响应模型
    """
    code: int = 0
    msg: str = "ok"
    data: Optional[T] = None


class ErrorResponse(BaseModel):
    """
    错误响应模型
    """
    code: int
    msg: str
    data: Optional[Any] = None


# 预定义的成功响应
def success_response(data: Optional[T] = None, msg: str = "ok") -> ResponseModel[T]:
    """
    创建成功响应
    """
    return ResponseModel(code=0, msg=msg, data=data)


# 预定义的错误响应
def error_response(code: int, msg: str, data: Optional[Any] = None) -> ErrorResponse:
    """
    创建错误响应
    """
    return ErrorResponse(code=code, msg=msg, data=data)
