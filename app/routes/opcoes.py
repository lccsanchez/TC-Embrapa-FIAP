"""Rotas de operações internas e importação/exportação."""

from fastapi import APIRouter, Depends

from app.service import auth_service, imp_exp_service
from app.service import op_internas_service as service

router = APIRouter()


@router.get("/info")
async def root():
    """Endpoint de status da API."""
    return {"message": "API em execução"}


@router.get("/producao")
async def get_prod(year: str, _=Depends(auth_service.get_current_user)):
    """Consulta produção."""
    return service.find(year, "producao")


@router.post("/save-producao")
async def save_all_pro(_=Depends(auth_service.get_current_user)):
    """Salva todos os dados de produção."""
    return service.save_all("producao")


@router.get("/comercializacao")
async def get_com(year: str, _=Depends(auth_service.get_current_user)):
    """Consulta comercialização."""
    return service.find(year, "comercio")


@router.post("/save-comercializacao")
async def save_all_com(_=Depends(auth_service.get_current_user)):
    """Salva todos os dados de comercialização."""
    return service.save_all("comercio")


@router.get("/processamento")
async def get_pro(year: str, subopcao: str, _=Depends(auth_service.get_current_user)):
    """Consulta processamento."""
    return service.find(year, "processamento", subopcao)


@router.post("/save-processamento")
async def save_all_pro(_=Depends(auth_service.get_current_user)):
    """Salva todos os dados de processamento."""
    return service.save_all("processamento")


@router.get("/importacao")
async def get_imp(year: str, subopcao: str, _=Depends(auth_service.get_current_user)):
    """Consulta importação."""
    return imp_exp_service.find(year, "importacao", subopcao)


@router.post("/save-importacao")
async def save_all_imp(_=Depends(auth_service.get_current_user)):
    """Salva todos os dados de importação."""
    return imp_exp_service.save_all("importacao")


@router.get("/exportacao")
async def get_exp(year: str, subopcao: str, _=Depends(auth_service.get_current_user)):
    """Consulta exportação."""
    return imp_exp_service.find(year, "exportacao", subopcao)


@router.post("/save-exportacao")
async def save_all_exp(_=Depends(auth_service.get_current_user)):
    """Salva todos os dados de exportação."""
    return imp_exp_service.save_all("exportacao")
