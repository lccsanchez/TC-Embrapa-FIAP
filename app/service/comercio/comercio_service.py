from repository.comercio import comercio_embrapa_repository, comercio_db_repository

def find_all():

    result = comercio_embrapa_repository.find_all()
    if result is None:
        result = comercio_db_repository.find_all() 
        print("(find_all) Obtendo o dado do database")    
    else:    
        print("(find_all) Obtendo o dado da embrapa")
    
    return result

def find_by_year(year):
    
    result = comercio_embrapa_repository.find_by_year(year)
    if result is None:
        result = comercio_db_repository.find_by_year(year)
        print("(find_by_year) Obtendo o dado do database")   
    else:
         print("(find_by_year) Obtendo o dado da embrapa")

    return result

def save_all():
    comercio_db_repository.add_all(comercio_embrapa_repository.find_all())
    