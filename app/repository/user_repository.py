from dotenv import load_dotenv
from os import getenv
from app.database import SessionLocal
from passlib.context import CryptContext
from fastapi.security import  OAuth2PasswordBearer
from model.entidades import Users
from dto.user import UserDTO

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

session =SessionLocal()

def authenticate_user(username: str, password: str):
    user = session.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_user(user: UserDTO):
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