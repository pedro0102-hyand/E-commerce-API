from datetime import datetime, timedelta, timezone # tempo do token expirar
from typing import Optional
from jose import JWTError, jwt # decodifica o token
from app.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):

    to_encode = data.copy() # copia dos dados

    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # geracao do token
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload # retorna dados, se o token for valido
    except JWTError:
        return None

