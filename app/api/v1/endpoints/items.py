from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from app.schemas.item import Item, ItemCreate, ItemUpdate

router = APIRouter()

# 模拟数据库
fake_items_db = {}
item_id_counter = 1


@router.get("/", response_model=List[Item])
async def get_items(skip: int = 0, limit: int = 10):
    """
    获取所有物品列表
    """
    items = list(fake_items_db.values())
    return items[skip: skip + limit]


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """
    根据ID获取物品
    """
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_items_db[item_id]


@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    """
    创建新物品
    """
    global item_id_counter
    new_item = Item(
        id=item_id_counter,
        created_at=datetime.now(),
        updated_at=None,
        **item.model_dump()
    )
    fake_items_db[item_id_counter] = new_item
    item_id_counter += 1
    return new_item


@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemUpdate):
    """
    更新物品信息
    """
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    stored_item = fake_items_db[item_id]
    update_data = item.model_dump(exclude_unset=True)
    update_data['updated_at'] = datetime.now()
    updated_item = stored_item.model_copy(update=update_data)
    fake_items_db[item_id] = updated_item
    return updated_item


@router.delete("/{item_id}")
async def delete_item(item_id: int):
    """
    删除物品
    """
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del fake_items_db[item_id]
    return {"message": "Item deleted successfully"}
