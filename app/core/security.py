from datetime import datetime, timedelta
from typing import Optional


import anyio.to_thread
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


ALGORITHM = settings.ALGORITHM
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: str, expires_delta: timedelta = None) -> str:
    """
    创建访问令牌
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_access_token(token: str) -> Optional[str]:
    """
    验证访问令牌并返回用户名
    """
    try:
        payload = await anyio.to_thread.run_sync(
            jwt.decode, token, settings.SECRET_KEY, ALGORITHM
        )

        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None
