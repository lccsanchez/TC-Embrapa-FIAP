from typing import List,Tuple
import pandas as pd

from urls import urls_processamento,separador_processamento
from app.util import collections, etl
from dto import ProcessamentoDto, RegistrosDto 


def find_all() -> List[ProcessamentoDto] | None:   
    try:
        return etl.execute(urls_processamento,separador_processamento, __converter)
    except Exception as e:
        print(f"[Erro] método find_all: {e}")
        return None


def find_by_year(year: int, classificacao:str) -> List[ProcessamentoDto] | None:
    try:
        data = etl.execute(urls_processamento,separador_processamento, __converter)

        if data is None:
            return None
        
        if(not classificacao is None):
            data = collections.filter(data, lambda processamento: processamento.classificacao==classificacao)

        if(not year is None):
            for item in data:
                item.registros = collections.filter(
                    item.registros,

                    lambda registro: int(registro.ano) == int(year)

                    lambda registro: registro.ano == int(year)

                )
        return data
    except Exception as e:
        print(f"[Erro] método find_by_year: {e}")
        return None

def __converter(dataframes: List[Tuple[str, pd.DataFrame]]) -> List[ProcessamentoDto]:
   
    producoes = []
    
    try:
        for key, df in dataframes:                     
            ano_colunas = [col for col in df.columns if str(col).isdigit() and len(str(col)) == 4]
            classification = key       
            for _, row in df.iterrows():              
                producao_anos = [
                    RegistrosDto(ano=ano, quantidade=0 if not str(row[ano]).isdigit() else (row[ano]))
                    for ano in ano_colunas
                    if pd.notna(row[ano])
                ]
                
                if producao_anos:
                    producoes.append(ProcessamentoDto(
                        id=str(row['id']),
                        control=row['control'],
                        produto=row['cultivar'],
                        classificacao="" if classification is None else classification ,
                        registros=producao_anos
                    ))
        
        return producoes
    
    except (ValueError, KeyError) as e:
        print(f"[Erro de Dados] Verifique a estrutura do DataFrame: {e}")
        return None
    except Exception as e:
        print(f"[Erro Inesperado] método __converter: {e}")
        return None