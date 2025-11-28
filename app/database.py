from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# 创建异步数据库引擎
# 根据数据库类型选择驱动
if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite 配置
    engine = create_async_engine(
        settings.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://"),
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False}  # SQLite 需要这个参数
    )
elif settings.DATABASE_URL.startswith("mysql"):
    # MySQL 配置（使用 aiomysql）
    engine = create_async_engine(
        settings.DATABASE_URL.replace("mysql://", "mysql+aiomysql://"),
        echo=settings.DEBUG,
        # 连接池配置
        pool_size=20,              # 基础连接池大小
        max_overflow=30,           # 超过 pool_size 的额外连接
        pool_pre_ping=True,        # 验证连接有效性
        pool_recycle=3600,         # 连接回收时间(秒)
    )
else:
    # 默认配置（适用于 PostgreSQL 等）
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        # 连接池配置
        pool_size=20,
        max_overflow=30,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    """
    获取异步数据库会话的依赖函数
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables():
    """
    创建所有数据库表
    """
    from app.models.base import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
