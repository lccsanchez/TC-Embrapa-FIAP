from fastapi import APIRouter, Depends
from app.service import auth_service
import app.service.producao.producao_service as ps

router = APIRouter()  


@router.get("/")
async def root():
    return {"message": "API em execução"}


@router.get("/producao")
async def get_items(year: str, _ = Depends(auth_service.get_current_user)):
    
    return ps.find_by_year(year)
    
@router.post("/producao")
async def save_all( _ = Depends(auth_service.get_current_user)):
    
    return ps.save_all()    

# @router.get("/comercializacao")
# async def get_items(ano: str, _: dict = Depends(auth_service.get_current_user)):
   
#     cod_opcao = sessions["Comercialização"]
#     html_content = site.request(ano, cod_opcao)
#     response = site.scraping(WithSubItems(), html_content)
#     return response


# @router.get("/processamento")
# async def get_items( ano: str, subopcao: str = None,  _: dict = Depends(auth_service.get_current_user)):
  
#     cod_opcao = sessions["Processamento"]["item"]
#     cod_subopcao = sessions["Processamento"]["sub"].get(subopcao)
#     html_content = site.request(ano, cod_opcao, cod_subopcao)
#     response = site.scraping(WithSubItems(), html_content)
#     return response


# @router.get("/exportacao")
# async def get_items(ano: str, subopcao: str = None,  _: dict = Depends(auth_service.get_current_user)):
 
#     cod_opcao = sessions["Exportação"]["item"]
#     cod_subopcao = sessions["Exportação"]["sub"].get(subopcao)
#     html_content = site.request(ano, cod_opcao, cod_subopcao)
#     response = site.scraping(JustItems(), html_content)
#     return response


# @router.get("/importacao")
# async def get_items( ano: str, subopcao: str = None, _: dict = Depends(auth_service.get_current_user)):
     
#     cod_opcao = sessions["Importação"]["item"]
#     cod_subopcao = sessions["Importação"]["sub"].get(subopcao)
#     html_content = site.request(ano, cod_opcao, cod_subopcao)
#     response = site.scraping(JustItems(), html_content)
#     return response
