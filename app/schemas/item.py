from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ItemBase(BaseModel):
    """
    物品基础模型
    """
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    is_available: bool = True


class ItemCreate(ItemBase):
    """
    创建物品时使用
    """
    pass


class ItemUpdate(BaseModel):
    """
    更新物品时使用
    """
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    is_available: Optional[bool] = None


class Item(ItemBase):
    """
    物品完整模型
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
