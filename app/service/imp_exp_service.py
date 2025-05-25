"""Serviço para operações de importação e exportação."""

from fastapi import HTTPException

from app.model import model
from app.repository import (imp_exp_db_repository, imp_exp_embrapa_repository,
                            scapper_repository)
from app.util.url.gerenciamento_estado import estado
from app.util.url.urls_download import urls_exportacao, urls_importacao


def find(year, opcao, subopcao=None):
    """
    Busca os dados via scrapper ou via banco de dados.
    """
    subopcao = opcao if not subopcao else subopcao

    result = scapper_repository.find_with_justitems(year, opcao, subopcao)

    if result is None:
        result = imp_exp_db_repository.find(
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

    imp_exp_db_repository.add_all(
        tipo_operacao,
        imp_exp_embrapa_repository.find_all(tipo_registro, tipo_operacao, url),
    )

    return "Registros carregados com sucesso"


def _get_tipo_registro(tipo_operacao: str):
    """
    Retorna o tipo de registro de acordo com a operação.
    """
    if tipo_operacao == "importacao":
        return model.RegistroImportacao
    return model.RegistroExportacao


def _get_tipo_url(tipo_operacao: str):
    """
    Retorna a URL de acordo com a operação.
    """
    if tipo_operacao == "importacao":
        return urls_importacao
    return urls_exportacao
