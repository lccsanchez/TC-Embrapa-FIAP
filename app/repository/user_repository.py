from dotenv import load_dotenv
from os import getenv
from fastapi import HTTPException
from passlib.context import CryptContext
from fastapi.security import  OAuth2PasswordBearer
from app.model import Users
from app.dto.user import UserDTO
from sqlalchemy.exc import IntegrityError
from app.database import SessionLocal

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

def create_user(user: UserDTO):
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
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Usuário já existe."
        )
    except Exception as e:
        print(f"Erro no método create_user: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Não foi possível criar o usuário. Verifique os dados e tente novamente. {str.replace(str (e), create_user_model.hashed_password, "********")}"
        )

def authenticate_user(username: str, password: str):
    with SessionLocal() as session:
        user = session.query(Users).filter(Users.username == username).first()
        if not user:
            return False
        if not bcrypt_context.verify(password, user.hashed_password):
            return False
        return user
