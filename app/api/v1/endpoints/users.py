from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from app.schemas.user import User, UserCreate, UserUpdate

router = APIRouter()

# 模拟数据库
fake_users_db = {}
user_id_counter = 1


@router.get("/", response_model=List[User])
async def get_users(skip: int = 0, limit: int = 10):
    """
    获取所有用户列表
    """
    users = list(fake_users_db.values())
    return users[skip: skip + limit]


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """
    根据ID获取用户
    """
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return fake_users_db[user_id]


@router.post("/", response_model=User, status_code=201)
async def create_user(user: UserCreate):
    """
    创建新用户
    """
    global user_id_counter
    new_user = User(
        id=user_id_counter,
        created_at=datetime.now(),
        updated_at=None,
        **user.model_dump()
    )
    fake_users_db[user_id_counter] = new_user
    user_id_counter += 1
    return new_user


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate):
    """
    更新用户信息
    """
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    stored_user = fake_users_db[user_id]
    update_data = user.model_dump(exclude_unset=True)
    update_data['updated_at'] = datetime.now()
    updated_user = stored_user.model_copy(update=update_data)
    fake_users_db[user_id] = updated_user
    return updated_user


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """
    删除用户
    """
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del fake_users_db[user_id]
    return {"message": "User deleted successfully"}
