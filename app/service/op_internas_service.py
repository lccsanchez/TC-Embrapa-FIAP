from app.repository import scapper_repository
from app.repository import op_internas_embrapa_repository
from app.repository import op_internas_db_repository
from app.urls_download import url_producao, url_comercializacao, urls_processamento
import app.model as model

def find(year, opcao,subopcao=None):  

    subopcao = opcao if not subopcao else subopcao

    result = scapper_repository.find_with_subitems(year,opcao,subopcao)

    if result is None:
       
        result = op_internas_db_repository.find(year,__get_tipo_registro(opcao),opcao,subopcao)

        print("(find_by_year) Obtendo o dado do database")   
    else:
         print("(find_by_year) Obtendo o dado da embrapa (via scapping)")

    return result

def save_all(tipo_operacao):
   tipo_registro = __get_tipo_registro(tipo_operacao)
   url= __get_tipo_url(tipo_operacao)
   
   op_internas_db_repository.add_all(tipo_operacao,op_internas_embrapa_repository.find_all(tipo_registro,tipo_operacao,url))
   
   return None

def __get_tipo_registro(tipo_operacao: str):     
    if tipo_operacao=="producao":
        return model.RegistroProducao
        
    elif tipo_operacao=="comercio":
        return model.RegistroComercio
    else:
        return model.RegistroProcessamento
    
def __get_tipo_url(tipo_operacao: str):
    if tipo_operacao=="producao":
        return url_producao
        
    elif tipo_operacao=="comercio":
        return url_comercializacao
    else:
        return urls_processamento
    