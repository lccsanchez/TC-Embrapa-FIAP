from fastapi import APIRouter, Depends
from app.service import auth_service
import app.service.op_internas_service as service
import app.service.imp_exp_service as imp_exp_service


router = APIRouter()  

@router.get("/")
async def root():
    return {"message": "API em execução"}


@router.get("/producao")
async def get_prod(year: str, _ = Depends(auth_service.get_current_user)):
    return service.find(year,"producao")


@router.post("/save_producao")
async def save_all_pro( _ = Depends(auth_service.get_current_user)):
    return service.save_all("producao")


@router.get("/comercializacao")
async def get_com(year: str, _ = Depends(auth_service.get_current_user)):    
    return service.find(year,"comercio")

@router.post("/save_comercializacao")
async def save_all_com( _ = Depends(auth_service.get_current_user)):    
    return service.save_all("comercio")


@router.get("/processamento")
async def get_pro(year: str, subopcao: str, _ = Depends(auth_service.get_current_user)):
    return service.find(year,"processamento",subopcao)


@router.post("/save_processamento")
async def save_all_pro(_ = Depends(auth_service.get_current_user)):
    return service.save_all("processamento")


@router.get("/importacao")
async def get_imp(year: str, subopcao: str, _ = Depends(auth_service.get_current_user)):
    return imp_exp_service.find(year, "importacao", subopcao)


@router.post("/save_importacao")
async def save_all_imp( _ = Depends(auth_service.get_current_user)):
    return imp_exp_service.save_all("importacao")


@router.get("/exportacao")
async def get_exp(year: str, subopcao: str, _ = Depends(auth_service.get_current_user)):
    return imp_exp_service.find(year, "exportacao", subopcao)


@router.post("/save_exportacao")
async def save_all_exp( _ = Depends(auth_service.get_current_user)):
    return imp_exp_service.save_all("exportacao")
