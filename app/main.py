from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.v1.api import api_router
from app.database import create_tables
from app.schemas.response import error_response

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 设置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """
    应用启动时创建数据库表
    """
    await create_tables()

# 全局异常处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    HTTP异常统一处理
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            code=exc.status_code,
            msg=exc.detail,
            data=None
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    通用异常统一处理
    """
    return JSONResponse(
        status_code=500,
        content=error_response(
            code=500,
            msg="Internal Server Error",
            data=str(exc) if settings.DEBUG else None
        ).model_dump()
    )


# 注册路由
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """
    根路径
    """
    return {
        "message": "Welcome to FastAPI",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    健康检查
    """
    return {"status": "healthy"}
