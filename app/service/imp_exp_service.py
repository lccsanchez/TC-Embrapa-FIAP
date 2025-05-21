from app.repository import scapper_repository
from app.repository import imp_exp_embrapa_repository
from app.repository import imp_exp_db_repository
from app.urls_download import urls_importacao, urls_exportacao
import app.model as model


def find(year, opcao, subopcao=None):

    subopcao = opcao if not subopcao else subopcao

    result = scapper_repository.find_with_justitems(year, opcao, subopcao)

    if result is None:

        result = imp_exp_db_repository.find(
            year, __get_tipo_registro(opcao), opcao, subopcao
        )

        print("(find_by_year) Obtendo o dado do database")
    else:
        print("(find_by_year) Obtendo o dado da embrapa (via scapping)")

    return result


def save_all(tipo_operacao):
    tipo_registro = __get_tipo_registro(tipo_operacao)
    url = __get_tipo_url(tipo_operacao)

    imp_exp_db_repository.add_all(
        tipo_operacao,
        imp_exp_embrapa_repository.find_all(tipo_registro, tipo_operacao, url),
    )

    return None


def __get_tipo_registro(tipo_operacao: str):
    if tipo_operacao == "importacao":
        return model.RegistroImportacao
    else:
        return model.RegistroExportacao


def __get_tipo_url(tipo_operacao: str):
    if tipo_operacao == "importacao":
        return urls_importacao
    else:
        return urls_exportacao
