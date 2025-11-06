from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.schemas.response import ResponseModel, success_response
from app.crud.item import crud_item
from app.database import get_db

router = APIRouter()


@router.get("/", response_model=ResponseModel[List[Item]])
async def get_items(
    skip: int = 0, 
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    获取所有物品列表
    """
    items = await crud_item.get_multi(db, skip=skip, limit=limit)
    return success_response(data=items)


@router.get("/{item_id}", response_model=ResponseModel[Item])
async def get_item(
    item_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    根据ID获取物品
    """
    item = await crud_item.get(db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return success_response(data=item)


@router.post("/", response_model=ResponseModel[Item], status_code=201)
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建新物品
    """
    created_item = await crud_item.create(db, obj_in=item)
    return success_response(data=created_item, msg="Item created successfully")


@router.put("/{item_id}", response_model=ResponseModel[Item])
async def update_item(
    item_id: int,
    item: ItemUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    更新物品信息
    """
    db_item = await crud_item.get(db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item = await crud_item.update(db, db_obj=db_item, obj_in=item)
    return success_response(data=updated_item, msg="Item updated successfully")


@router.delete("/{item_id}", response_model=ResponseModel[dict])
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    删除物品
    """
    db_item = await crud_item.get(db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    await crud_item.delete(db, item_id=item_id)
    return success_response(data=None, msg="Item deleted successfully")
