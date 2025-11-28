from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.exceptions import NotFoundException, BusinessException
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.exceptions import NotFoundException, BusinessException
from app.schemas.user import User, UserCreate, UserUpdate, UserLogin, Token
from app.schemas.response import ResponseModel, success_response
from app.crud.user import crud_user
from app.database import get_db
from app.core.security import create_access_token
from app.api import deps

router = APIRouter()

@router.post("/login", response_model=ResponseModel[Token])
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    用户登录
    """
    user = await crud_user.authenticate(db, username=login_data.username, password=login_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(subject=user.username)
    return success_response(data=Token(access_token=access_token))



@router.get("/", response_model=ResponseModel[List[User]])
async def get_users(
    current_user: User = Depends(deps.get_current_user),
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
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    根据ID获取用户
    """
    user = await crud_user.get(db, user_id=user_id)
    if not user:
        raise NotFoundException(message="User not found")
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
        raise BusinessException(message="Username already registered")

    # 检查邮箱是否已存在
    if await crud_user.get_by_email(db, email=user.email):
        raise BusinessException(message="Email already registered")

    created_user = await crud_user.create(db, obj_in=user)
    return success_response(data=created_user, msg="User created successfully")


@router.put("/{user_id}", response_model=ResponseModel[User])
async def update_user(
    user_id: int,
    user: UserUpdate,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新用户信息
    """
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    db_user = await crud_user.get(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = await crud_user.update(db, db_obj=db_user, obj_in=user)
    return success_response(data=updated_user, msg="User updated successfully")


@router.delete("/{user_id}", response_model=ResponseModel[dict])
async def delete_user(
    user_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除用户
    """
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    db_user = await crud_user.get(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    await crud_user.delete(db, user_id=user_id)
    return success_response(data=None, msg="User deleted successfully")
