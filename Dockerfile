FROM python:3.11-slim

WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir --upgrade pip \
    && pip install -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 创建非root用户
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
