# FastAPI 项目模板

这是一个使用 FastAPI 构建的现代化 RESTful API 项目模板，包含了完整的项目结构和最佳实践。

## 项目结构

```
fastapi_demo/
├── app/
│   ├── __init__.py
│   ├── main.py                  # 应用入口文件
│   ├── core/                    # 核心模块
│   │   ├── __init__.py
│   │   └── config.py            # 应用配置
│   ├── api/                     # API 路由
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py           # 主路由聚合器
│   │       └── endpoints/       # 具体端点
│   │           ├── __init__.py
│   │           ├── items.py     # 物品相关接口
│   │           └── users.py     # 用户相关接口
│   └── schemas/                 # 数据模型
│       ├── __init__.py
│       ├── item.py              # 物品数据模型
│       └── user.py              # 用户数据模型
├── requirements.txt             # 依赖包
├── .env                         # 环境变量
├── .gitignore                   # Git 忽略文件
├── Dockerfile                   # Docker 构建文件
├── docker-compose.yml           # Docker Compose 配置
└── README.md                    # 项目文档
```

## 功能特性

- ✅ FastAPI 框架 - 现代化高性能 Web 框架
- ✅ Pydantic 数据验证 - 强类型数据模型
- ✅ 自动化 API 文档 - Swagger UI 和 ReDoc
- ✅ 模块化项目结构 - 易于扩展和维护
- ✅ 配置管理 - 基于环境变量
- ✅ CORS 支持 - 跨域资源共享
- ✅ 错误处理 - 统一的异常处理机制
- ✅ 数据模型分离 - 业务逻辑与数据模型解耦
- ✅ Docker 支持 - 容器化部署
- ✅ 完整的 CRUD 接口示例

## 快速开始

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd fastapi_demo
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\\Scripts\\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

创建 `.env` 文件并配置必要的环境变量：

```env
PROJECT_NAME=FastAPI Template
VERSION=1.0.0
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. 运行应用

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. 访问应用

- 应用地址: http://localhost:8000
- API 文档: http://localhost:8000/docs
- ReDoc 文档: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health

## API 端点

### 用户相关接口
- `GET /api/v1/users/` - 获取用户列表
- `GET /api/v1/users/{user_id}` - 获取单个用户
- `POST /api/v1/users/` - 创建新用户
- `PUT /api/v1/users/{user_id}` - 更新用户信息
- `DELETE /api/v1/users/{user_id}` - 删除用户

### 物品相关接口
- `GET /api/v1/items/` - 获取物品列表
- `GET /api/v1/items/{item_id}` - 获取单个物品
- `POST /api/v1/items/` - 创建新物品
- `PUT /api/v1/items/{item_id}` - 更新物品信息
- `DELETE /api/v1/items/{item_id}` - 删除物品

## 开发指南

### 添加新的 API 端点

1. 在 `app/api/v1/endpoints/` 目录下创建新的路由文件
2. 定义路由和对应的 schemas
3. 在 `app/api/v1/api.py` 中注册新路由

### 修改数据模型

1. 在 `app/schemas/` 目录下修改或创建新的模型
2. 更新相关的 API 端点以使用新的模型

### 配置管理

- 应用配置位于 `app/core/config.py`
- 支持通过环境变量或 `.env` 文件进行配置
- 生产环境请修改默认的密钥和配置

## Docker 部署

### 构建镜像

```bash
docker build -t fastapi-demo .
```

### 使用 Docker Compose

```bash
docker-compose up -d
```

## 测试

运行测试：

```bash
pytest
```

## 环境要求

- Python 3.8+
- FastAPI 0.109.0
- Uvicorn 0.27.0
- SQLAlchemy 2.0.25
- Pydantic 2.5.3

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Pull Request 和 Issue！
