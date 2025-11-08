from typing import Any


class BusinessException(Exception):
    def __init__(self, message: str, code: int = 400, data: Any = None):
        self.message = message
        self.code = code
        self.data = data
        super().__init__(self.message)

class NotFoundException(BusinessException):
    def __init__(self, message: str = "资源不存在", data: Any = None):
        super().__init__(message, 404, data)

class UnauthorizedException(BusinessException):
    def __init__(self, message: str = "未授权访问", data: Any = None):
        super().__init__(message, 401, data)