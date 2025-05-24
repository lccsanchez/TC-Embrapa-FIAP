from typing import TypeVar,Tuple,List
import pandas as pd 
from  app.util import csv

T = TypeVar('T') 

def __load(url: str) -> pd.DataFrame:

    print(f'A url final é {url}')

    if url is None:        
        print(f"Erro ao buscar o CSV para {url}.")
        return None

    try:
        csv_dataframe = csv.read(url,10)

        print(f'CSV carregado com sucesso: {url}')

        return csv_dataframe

    except Exception as e:
        print(f"Erro ao transformar {url}: {e}")
       
        return None

def execute(urls_dict: dict) -> List[Tuple[str,pd.DataFrame]]:  

    dataframes : List[Tuple[str,pd.DataFrame]] = []

    for key, url in urls_dict.items():

        print(f'Executando leitura de  {key} URL: {url}')


        dataframe = __load(url,key)
        
        if dataframe is None or dataframe.empty:
            return None

        dataframes.append((key,dataframe))

        if len(dataframes)==0:
            print("Nenhum dado foi processado.")
            return None


    return dataframes