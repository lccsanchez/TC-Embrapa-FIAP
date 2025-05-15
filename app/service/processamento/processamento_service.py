from app.repository.processamento import processamento_embrapa_repository
from app.repository.processamento import processamento_db_repository

def find_all():

    result = processamento_embrapa_repository.find_all()
    if result is None:
        #result = producao_db_repository.find_all() 
        print("(find_all) Obtendo o dado do database")    
    else:    
        print("(find_all) Obtendo o dado da embrapa")
    
    return result

def find_by_year(year,classification):
    
    result = processamento_embrapa_repository.find_by_year(year,classification)
    if result is None :
        result = processamento_db_repository.find_by_year(year,classification)
        print("(find_by_year) Obtendo o dado do database")   
    else:
         print("(find_by_year) Obtendo o dado da embrapa")

    return result

def save_all():
    
    processamento_db_repository.add_all(processamento_embrapa_repository.find_all())
    return "OK"
    