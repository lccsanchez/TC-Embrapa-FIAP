from fastapi import HTTPException
from app.repository import scapper_repository
from app.repository import op_internas_embrapa_repository
from app.repository import op_internas_db_repository
from app.urls_download import url_producao, url_comercializacao, urls_processamento
import app.model as model

def find(year, opcao,subopcao=None):  
    """
    Busca os dados via scrapper ou via banco de dados.
    """
    result = scapper_repository.find_with_subitems(year,opcao,subopcao)

    if result is None:
       
        result = op_internas_db_repository.find(year,__get_tipo_registro(opcao),opcao,subopcao)

        print("(find_by_year) Obtendo o dado do database")   
    else:
         print("(find_by_year) Obtendo o dado da embrapa (via scapping)")

    if not result:
        raise HTTPException(status_code=404, detail="Registros não localizados") 
    
    return result

def save_all(tipo_operacao):
    """
    Salva todos os dados no banco de dados.
    """
    tipo_registro = __get_tipo_registro(tipo_operacao)
    url= __get_tipo_url(tipo_operacao)
   
    op_internas_db_repository.add_all(tipo_operacao,op_internas_embrapa_repository.find_all(tipo_registro,tipo_operacao,url))
   
    return "Registros carregados com sucesso"

def __get_tipo_registro(tipo_operacao: str):  
    """
    Retorna o tipo de registro de acordo com a operação.
    """   
    if tipo_operacao=="producao":
        return model.RegistroProducao
        
    elif tipo_operacao=="comercio":
        return model.RegistroComercio
    else:
        return model.RegistroProcessamento
    
def __get_tipo_url(tipo_operacao: str):
    """
    Retorna a URL de acordo com a operação.
    """
    if tipo_operacao=="producao":
        return url_producao
        
    elif tipo_operacao=="comercio":
        return url_comercializacao
    else:
        return urls_processamento
    