from app.repository.importacao import importacao_embrapa_repository, importacao_db_repository


def find_all():

    result = importacao_embrapa_repository.find_all()
    if result is None:
        result = importacao_db_repository.find_all()
        print("(find_all) Obtendo o dado do database")
    else:
        print("(find_all) Obtendo o dado da embrapa")

    return result


def find_by_year(year, classification):

    result = importacao_embrapa_repository.find_by_year(year, classification)
    if result is None:
        result = importacao_db_repository.find_by_year(year, classification)
        print("(find_by_year) Obtendo o dado do database")
    else:
        print("(find_by_year) Obtendo o dado da embrapa")

    return result


def save_all():
    importacao_db_repository.add_all(importacao_embrapa_repository.find_all())
    return "OK"
