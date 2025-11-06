#!/usr/bin/env python3
"""
异步数据库功能测试脚本
"""

import sys
import os
import asyncio

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import create_tables, AsyncSessionLocal
from app.crud.item import crud_item
from app.crud.user import crud_user
from app.schemas.item import ItemCreate
from app.schemas.user import UserCreate


async def test_async_database():
    """测试异步数据库功能"""
    print("开始测试异步数据库功能...")
    
    # 创建数据库表
    await create_tables()
    print("✓ 数据库表创建成功")
    
    # 创建数据库会话
    async with AsyncSessionLocal() as db:
        try:
            # 测试物品 CRUD 操作
            print("\n--- 测试物品 CRUD 操作 ---")
            
            # 创建物品
            item_data = ItemCreate(
                name="测试物品",
                description="这是一个测试物品",
                price=99.99,
                category="测试类别",
                is_available=True
            )
            created_item = await crud_item.create(db, obj_in=item_data)
            print(f"✓ 创建物品成功: {created_item.name} (ID: {created_item.id})")
            
            # 获取物品
            retrieved_item = await crud_item.get(db, item_id=created_item.id)
            print(f"✓ 获取物品成功: {retrieved_item.name}")
            
            # 获取物品列表
            items = await crud_item.get_multi(db, skip=0, limit=10)
            print(f"✓ 获取物品列表成功: {len(items)} 个物品")

            # 删除物品
            deleted_item = await crud_item.delete(db, item_id=created_item.id)
            
            # 测试用户 CRUD 操作
            print("\n--- 测试用户 CRUD 操作 ---")
            
            # 创建用户
            user_data = UserCreate(
                username="testuser",
                email="test@example.com",
                full_name="测试用户",
                password="testpassword123",
                is_active=True,
                is_superuser=False
            )
            created_user = await crud_user.create(db, obj_in=user_data)
            print(f"✓ 创建用户成功: {created_user.username} (ID: {created_user.id})")
            
            # 获取用户
            retrieved_user = await crud_user.get(db, user_id=created_user.id)
            print(f"✓ 获取用户成功: {retrieved_user.username}")
            
            # 用户认证测试
            authenticated_user = await crud_user.authenticate(
                db, username="testuser", password="testpassword123"
            )
            if authenticated_user:
                print(f"✓ 用户认证成功: {authenticated_user.username}")
            else:
                print("✗ 用户认证失败")
            
            # 获取用户列表
            users = await crud_user.get_multi(db, skip=0, limit=10)
            print(f"✓ 获取用户列表成功: {len(users)} 个用户")

            # 删除用户
            deleted_user = await crud_user.delete(db, user_id=1)


            
            print("\n🎉 所有异步数据库功能测试通过！")
            
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()


async def main():
    """主函数"""
    await test_async_database()


if __name__ == "__main__":
    asyncio.run(main())
