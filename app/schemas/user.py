from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """
    用户基础模型
    """
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    """
    创建用户时使用
    """
    password: str = Field(..., min_length=8, max_length=72, description="密码，最长72字节")


class UserUpdate(BaseModel):
    """
    更新用户时使用
    """
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class User(UserBase):
    """
    用户完整模型
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserInDB(User):
    """
    数据库用户模型(包含密码哈希)
    """
    hashed_password: str


class UserLogin(BaseModel):
    """
    用户登录模型
    """
    username: str
    password: str


class Token(BaseModel):
    """
    令牌模型
    """
    access_token: str
    token_type: str = "bearer"

