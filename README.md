# FastAPI 项目模板

这是一个使用 FastAPI 构建的现代化 RESTful API 项目模板，采用干净架构模式。支持异步数据库操作 (SQLAlchemy + aiosqlite)，清晰分离模型、schemas、CRUD 和 API 端点。

## 项目结构

```
fastapi_demo/
├── app/                          # 应用主目录
│   ├── __init__.py
│   ├── main.py                   # 应用入口
│   ├── database.py               # 数据库配置
│   ├── core/                     # 核心模块
│   │   ├── __init__.py
│   │   ├── config.py             # 配置
│   │   ├── security.py           # JWT 安全 (异步优化)
│   │   └── exceptions.py         # 自定义异常
│   ├── api/                      # API 路由
│   │   └── v1/
│   │       ├── api.py            # 路由聚合
│   │       └── endpoints/
│   │           ├── users.py      # 用户接口 (含登录)
│   │           └── items.py      # 物品接口
│   ├── models/                   # 数据库模型
│   │   ├── base.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/                  # Pydantic 模型
│   │   ├── user.py
│   │   ├── item.py
│   │   └── response.py
│   └── crud/                     # CRUD 操作
│       ├── user.py
│       └── item.py
├── requirements.txt
├── pyproject.toml                # Python 配置 (Python 3.11+)
├── uv.lock
├── .env.example
├── run.py                        # 启动脚本
├── test_database.py
├── test_async_database.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 架构说明

### 分层结构
1. **Models** (`app/models/`): SQLAlchemy ORM 模型
2. **Schemas** (`app/schemas/`): Pydantic 验证
3. **CRUD** (`app/crud/`): 数据库访问层
4. **API** (`app/api/`): REST 端点
5. **Core** (`app/core/`): 配置、安全、异常

### 数据库
- 异步 SQLite (SQLAlchemy async + aiosqlite)
- `get_db()` 依赖注入 AsyncSession
- 启动时自动建表

### 异常处理
三层处理 (`app/main.py`):
1. `BusinessException` → 200 + 错误码
2. `HTTPException` → HTTP 状态码
3. 通用 `Exception` → 500 (DEBUG 模式详细)

## 功能特性

- ✅ FastAPI 高性能框架
- ✅ Pydantic v2 验证
- ✅ 自动 OpenAPI 文档 (/docs, /redoc)
- ✅ 异步数据库操作
- ✅ **异步 JWT 认证** (非阻塞，anyio.to_thread 优化高并发)
- ✅ 自定义异常 & 统一响应
- ✅ CORS 支持
- ✅ Docker 部署
- ✅ UV 依赖管理 (推荐)

## 快速开始

### 1. 环境要求
Python 3.11+

### 2. 安装依赖 (推荐 UV)
```bash
uv pip install -r requirements.txt
# 或 pip install -r requirements.txt
```

### 3. 配置 .env
复制 `.env.example` → `.env`，修改 SECRET_KEY 等。

### 4. 运行
```bash
python run.py  # 开发模式 (reload)
# 或
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问: http://localhost:8000/docs

## API 端点 (前缀 /api/v1)

### 用户 (/users)
- `POST /login` - 登录获取 Token (UserLogin: username/password)
- `GET /` - 列表 (分页)
- `GET /{user_id}` - 获取
- `POST /` - 创建
- `PUT /{user_id}` - 更新
- `DELETE /{user_id}` - 删除

### 物品 (/items)
- `GET /` - 列表
- `GET /{item_id}` - 获取
- `POST /` - 创建
- `PUT /{item_id}` - 更新
- `DELETE /{item_id}` - 删除

### 工具
- `GET /` - 欢迎
- `GET /health` - 健康检查

## JWT 认证

1. **登录**:
```bash
curl -X POST http://localhost:8000/api/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'
```
返回 `{"access_token": "eyJ..."}`

2. **保护端点**:
```
Authorization: Bearer <access_token>
```

实现: `deps.py` get_current_user (await verify_access_token)，`security.py` 异步 JWT。

## 最近变更

- **73f71d0** feat(auth): 异步 JWT 验证 (anyio.to_thread 优化并发)
- **641ee08** fix(auth): get_current_user 检查用户活跃状态
- **7f44519** feat(auth): 用户认证 & 权限控制
- **f5e9c82** docs: 添加 CLAUDE.md
- **e4869a9** feat: 结构化异常处理

## 性能测试 (wrk)

安装: `brew install wrk`

登录压测:
```bash
echo 'wrk.method = "POST"
wrk.body   = '{"username":"test","password":"test"}'
wrk.headers["Content-Type"] = "application/json"' > post.lua

wrk -t12 -c400 -d30s -s post.lua http://localhost:8000/api/v1/users/login --latency
```

预期: Requests/sec >5k, P99 <50ms (异步后)。

## 开发命令

### 运行
```bash
python run.py  # 开发
uvicorn app.main:app  # 生产
```

### 测试
```bash
pytest  # 全部
pytest test_async_database.py -v  # 异步 DB
python test_database.py  # CRUD 测试
```

### Docker
```bash
docker build -t fastapi-demo .
docker-compose up -d
docker run -p 8000:8000 fastapi-demo
```

### 依赖 (UV 推荐)
```bash
uv pip install -r requirements.txt
```

## 配置

`app/core/config.py` (pydantic-settings):
- DATABASE_URL: sqlite:///./app.db
- SECRET_KEY, ALGORITHM=HS256, ACCESS_TOKEN_EXPIRE_MINUTES=30
- DEBUG, ALLOWED_ORIGINS 等

## 开发工作流

### 新资源
1. `app/models/{resource}.py`
2. `app/schemas/{resource}.py`
3. `app/crud/{resource}.py`
4. `app/api/v1/endpoints/{resource}.py`
5. 注册 `app/api/v1/api.py`

### 迁移 (Alembic)
```bash
alembic init alembic
alembic revision --autogenerate -m "desc"
alembic upgrade head
```

## 关键依赖 (pyproject.toml)

- FastAPI 0.109.0
- SQLAlchemy[asyncio] 2.0.25
- python-jose[cryptography] 3.3.0
- pydantic 2.5.3
- uvicorn[standard] 0.27.0
- anyio 4.11.0 (异步线程)

## 许可证 & 贡献

MIT 许可证。欢迎 PR！

🤖 Generated with [Claude Code](https://claude.com/claude-code)