from app.repository.exportacao import exportacao_embrapa_repository, exportacao_db_repository


def find_all():

    result = exportacao_embrapa_repository.find_all()
    if result is None:
        result = exportacao_db_repository.find_all()
        print("(find_all) Obtendo o dado do database")
    else:
        print("(find_all) Obtendo o dado da embrapa")

    return result


def find_by_year(year, classification):

    result = exportacao_embrapa_repository.find_by_year(year, classification)
    if result is None:
        result = exportacao_db_repository.find_by_year(year, classification)
        print("(find_by_year) Obtendo o dado do database")
    else:
        print("(find_by_year) Obtendo o dado da embrapa")

    return result


def save_all():

    exportacao_db_repository.add_all(exportacao_embrapa_repository.find_all())
    return "OK"
