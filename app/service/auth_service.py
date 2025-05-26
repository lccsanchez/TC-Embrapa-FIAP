"""Serviço de autenticação de usuários."""

from datetime import datetime, timedelta, timezone
from os import getenv
from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from starlette import status

from app.dto.user import UserDTO
from app.repository import user_repository

load_dotenv()
SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")

router = APIRouter(prefix="/auth", tags=["auth"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def authenticate_user(username: str, password: str):
    """
    Autentica o usuário e gera um token JWT.
    """
    user = user_repository.authenticate_user(username, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )

    token = create_access_token(
        user.username, user.id, user.role, timedelta(minutes=20)
    )

    return {"access_token": token, "token_type": "bearer"}


def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
):
    """
    Cria um token JWT com informações do usuário.
    """
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """
    Obtém o usuário atual a partir do token JWT.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return {"username": username, "id": user_id, "user_role": user_role}
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication Failed : {ex}",
        ) from ex


def create_user(user: UserDTO):
    """
    Cria um novo usuário no banco de dados.
    """
    user_repository.create_user(user)
