from repository.producao import producao_scapper_repository , producao_db_repository , producao_embrapa_repository


def find_by_year(year):
    
    result = producao_scapper_repository.find_by_year(year)
    if result is None:
        result = producao_db_repository.find_by_year(year)
        print("(find_by_year) Obtendo o dado do database")   
    else:
         print("(find_by_year) Obtendo o dado da embrapa (via scapping)")

    return result

def save_all():
    producao_db_repository.add_all(producao_embrapa_repository.find_all())
    return
    