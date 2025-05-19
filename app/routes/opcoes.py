from fastapi import APIRouter, Depends
from app.service import auth_service
import app.service.op_internas_service as service


router = APIRouter()  

@router.get("/")
async def root():
    return {"message": "API em execução"}


@router.get("/producao")
async def get_prod(year: str, _ = Depends(auth_service.get_current_user)):
        return service.find(year,"producao")

@router.post("/producao")
async def save_all_pro(_ = Depends(auth_service.get_current_user)):    
   return service.save_all("producao")

@router.get("/comercializacao")
async def get_com(year: str, _ = Depends(auth_service.get_current_user)):    
    return service.find(year,"comercio")

@router.post("/comercializacao")
async def save_all_com( _ = Depends(auth_service.get_current_user)):    
    return service.save_all("comercio")

@router.get("/processamento")
async def get_pro(year: str, subopcao: str, _ = Depends(auth_service.get_current_user)):    
    return service.find(year,"processamento",subopcao)
    
@router.post("/processamento")
async def save_all_pro( _ = Depends(auth_service.get_current_user)):
    
    return service.save_all("processamento")



