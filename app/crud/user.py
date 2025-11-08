from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.core.exceptions import BusinessException
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser:
    """
    用户 CRUD 操作
    """

    async def get(self, db: AsyncSession, user_id: int) -> Optional[User]:
        """
        根据ID获取用户
        """
        result = await db.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        """
        根据用户名获取用户
        """
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """
        根据邮箱获取用户
        """
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[User]:
        """
        获取用户列表
        """
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        """
        创建新用户
        """
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            full_name=obj_in.full_name,
            # hashed_password=User.get_password_hash(obj_in.password),
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser,
        )
        await db_obj.hash_password_async(obj_in.password)

        try:
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except Exception as e:
            await db.rollback()
            raise BusinessException(message=str(e))

    async def update(
        self, db: AsyncSession, *, db_obj: User, obj_in: UserUpdate
    ) -> User:
        """
        更新用户
        """
        update_data = obj_in.model_dump(exclude_unset=True)
        if "password" in update_data:
            hashed_password = User.get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, user_id: int) -> User:
        """
        删除用户
        """
        result = await db.execute(select(User).filter(User.id == user_id))
        obj = result.scalar_one_or_none()
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

    async def authenticate(
        self, db: AsyncSession, *, username: str, password: str
    ) -> Optional[User]:
        """
        用户认证
        """
        user = await self.get_by_username(db, username=username)
        if not user:
            return None
        if not user.verify_password(password):
            return None
        return user


crud_user = CRUDUser()
