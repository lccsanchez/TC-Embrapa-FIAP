
from typing import Annotated
from fastapi import APIRouter, Depends
from starlette import status
from app.dto.user import UserDTO
from app.dto.token import TokenDTO
from fastapi.security import OAuth2PasswordRequestForm
from app.service import auth_service 

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/create-user", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserDTO):  
    auth_service.create_user(user)      


@router.post("/token", response_model=TokenDTO)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    return  auth_service.authenticate_user(form_data.username, form_data.password)
     
    
