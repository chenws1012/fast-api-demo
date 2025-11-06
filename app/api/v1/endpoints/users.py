from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.user import User, UserCreate, UserUpdate
from app.schemas.response import ResponseModel, success_response
from app.crud.user import crud_user
from app.database import get_db

router = APIRouter()


@router.get("/", response_model=ResponseModel[List[User]])
async def get_users(
    skip: int = 0, 
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    获取所有用户列表
    """
    users = await crud_user.get_multi(db, skip=skip, limit=limit)
    return success_response(data=users)


@router.get("/{user_id}", response_model=ResponseModel[User])
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    根据ID获取用户
    """
    user = await crud_user.get(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return success_response(data=user)


@router.post("/", response_model=ResponseModel[User], status_code=201)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建新用户
    """
    # 检查用户名是否已存在
    if await crud_user.get_by_username(db, username=user.username):
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    # 检查邮箱是否已存在
    if await crud_user.get_by_email(db, email=user.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    created_user = await crud_user.create(db, obj_in=user)
    return success_response(data=created_user, msg="User created successfully")


@router.put("/{user_id}", response_model=ResponseModel[User])
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    更新用户信息
    """
    db_user = await crud_user.get(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = await crud_user.update(db, db_obj=db_user, obj_in=user)
    return success_response(data=updated_user, msg="User updated successfully")


@router.delete("/{user_id}", response_model=ResponseModel[dict])
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    删除用户
    """
    db_user = await crud_user.get(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    await crud_user.delete(db, user_id=user_id)
    return success_response(data=None, msg="User deleted successfully")
