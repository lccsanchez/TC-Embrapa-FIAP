"""Repositório para operações de usuário."""

from os import getenv
from dotenv import load_dotenv
from fastapi import HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError
from app.model.model import Users
from app.dto.user import UserDTO
from app.database.session import SessionLocal

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_user(user: UserDTO):
    """Cria um novo usuário no banco de dados."""
    try:
        with SessionLocal() as session:
            create_user_model = Users(
                email=user.email,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                role=user.role,
                hashed_password=bcrypt_context.hash(user.password),
                is_active=True,
                phone_number=user.phone_number,
            )
            session.add(create_user_model)
            session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Usuário ou e-mail já existente."
        ) from exc
    except Exception as exc:
        print(f"Erro no método create_user: {exc}")
        mensagem_erro = str(exc).replace(
            getattr(
                create_user_model,
                "hashed_password",
                "********"
            ),
            "********"
        )
        raise HTTPException(
            status_code=500,
            detail=(
                "Não foi possível criar o usuário. "
                "Verifique os dados e tente novamente. "
                f"{mensagem_erro}"
            )
        ) from exc


def authenticate_user(username: str, password: str):
    """Autentica um usuário pelo nome e senha."""
    with SessionLocal() as session:
        user = session.query(Users).filter(Users.username == username).first()
        if not user:
            return False
        if not bcrypt_context.verify(password, user.hashed_password):
            return False
        return user
