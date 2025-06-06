"""
Serviço para operações internas (produção, processamento, comercialização).
"""

from fastapi import HTTPException

from app.model import model
from app.repository import (
    op_internas_db_repository,
    op_internas_embrapa_repository,
    scapper_repository,
)
from app.util.url.gerenciamento_estado import estado
from app.util.url.urls_download import (
    url_comercializacao,
    url_producao,
    urls_processamento,
)


def find(year, opcao, subopcao=None):
    """
    Busca os dados via scrapper ou via banco de dados.
    """
    result = scapper_repository.find_with_subitems(year, opcao, subopcao)

    if result is None:
        result = op_internas_db_repository.find(
            year, _get_tipo_registro(opcao), opcao, subopcao
        )
        print("(find_by_year) Obtendo o dado do database")
        estado.repository = "database"
    else:
        print("(find_by_year) Obtendo o dado da embrapa (via scapping)")
        estado.repository = "scapping"

    if not result:
        raise HTTPException(status_code=404, detail="Registros não localizados")

    return result


def save_all(tipo_operacao):
    """
    Salva todos os dados no banco de dados.
    """
    tipo_registro = _get_tipo_registro(tipo_operacao)
    url = _get_tipo_url(tipo_operacao)

    items = op_internas_embrapa_repository.find_all(tipo_registro, tipo_operacao, url)
    
    if items:
        op_internas_db_repository.add_all(
        tipo_operacao,
        items)
        return "Registros carregados com sucesso"
    
    raise HTTPException(status_code=503, detail="Site do embrapa indisponível")
    

    


def _get_tipo_registro(tipo_operacao: str):
    """
    Retorna o tipo de registro de acordo com a operação.
    """
    if tipo_operacao == "producao":
        return model.RegistroProducao
    if tipo_operacao == "comercio":
        return model.RegistroComercio
    return model.RegistroProcessamento


def _get_tipo_url(tipo_operacao: str):
    """
    Retorna a URL de acordo com a operação.
    """
    if tipo_operacao == "producao":
        return url_producao
    if tipo_operacao == "comercio":
        return url_comercializacao
    return urls_processamento
