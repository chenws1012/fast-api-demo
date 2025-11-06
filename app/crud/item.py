from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class CRUDItem:
    """
    物品 CRUD 操作
    """

    async def get(self, db: AsyncSession, item_id: int) -> Optional[Item]:
        """
        根据ID获取物品
        """
        result = await db.execute(select(Item).filter(Item.id == item_id))
        return result.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        """
        获取物品列表
        """
        result = await db.execute(select(Item).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: ItemCreate) -> Item:
        """
        创建新物品
        """
        db_obj = Item(
            name=obj_in.name,
            description=obj_in.description,
            price=obj_in.price,
            category=obj_in.category,
            is_available=obj_in.is_available,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: Item, obj_in: ItemUpdate
    ) -> Item:
        """
        更新物品
        """
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, item_id: int) -> Item:
        """
        删除物品
        """
        result = await db.execute(select(Item).filter(Item.id == item_id))
        obj = result.scalar_one_or_none()
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj


crud_item = CRUDItem()
