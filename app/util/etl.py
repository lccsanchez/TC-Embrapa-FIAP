from typing import Callable, TypeVar,Tuple,List
import pandas as pd 
from  util import csv 

T = TypeVar('T') 

def __load(url: str,separator: str) -> pd.DataFrame:
      
    print(f'A url final é {url}')

    if url is None:        
        print(f"Erro ao buscar o CSV para {url}.")
        return None
    
    try:                     
        csv_datafreame =  csv.read(url)
                
        print(f'CSV carregado com sucesso: {url}')
        
        return csv_datafreame
    
    except Exception as e:
        print(f"Erro ao transformar {url}: {e}")

def execute(urls_dict: dict, separator: str, converter: Callable[[List[Tuple[str,pd.DataFrame]]], List[T]]) -> List[T]:  

    dataframes : List[Tuple[str,pd.DataFrame]] = []

    for key, url in urls_dict.items():
        
        print(f'Executando leitura de  {key} URL: {url}')

        dataframe = __load(url,separator)
        if not dataframe: 
            return None
        
        dataframes.append((key,dataframe))
   
        if len(dataframes)==0:
            print("Nenhum dado foi processado.")
            return None

    return converter(dataframes)

