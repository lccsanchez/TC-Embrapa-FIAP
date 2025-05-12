from typing import List,Tuple
import pandas as pd

from urls import url_producao,separador_producao
from app.util import collections, etl
from dto import ProducaoDto, RegistrosDto 


def find_all() -> List[ProducaoDto] | None:   
    try:
        return etl.execute(url_producao,separador_producao, __converter)
    except Exception as e:
        print(f"[Erro] método find_all: {e}")
        return None


def find_by_year(year: int) -> List[ProducaoDto] | None:
    try:
        data = etl.execute(url_producao,separador_producao, __converter)
        
        if not data:
            return None
        
        for item in data:
            item.registros = collections.filter(
                item.registros,
                lambda p: int(p.ano) == int(year)
            )
        return data
    except Exception as e:
        print(f"[Erro] método find_by_year: {e}")
        return None

def __converter(dataframes: List[Tuple[str, pd.DataFrame]]) -> List[ProducaoDto]:
   
    producoes = []
    
    try:
        for _, df in dataframes:          
            ano_colunas = [col for col in df.columns if str(col).isdigit() and len(str(col)) == 4]
                   
            for _, row in df.iterrows():              
                producao_anos = [
                    RegistrosDto(ano=ano, quantidade = 0 if not str(row[ano]).isdigit() else (row[ano]))
                    for ano in ano_colunas
                    if pd.notna(row[ano])
                ]
                
                if producao_anos:
                    producoes.append(ProducaoDto(
                        id=row['id'],
                        control=row['control'],
                        produto=row['produto'],
                        registros=producao_anos
                    ))
        
        return producoes
    
    except (ValueError, KeyError) as e:
        print(f"[Erro de Dados] Verifique a estrutura do DataFrame: {e}")
        return None
    except Exception as e:
        print(f"[Erro Inesperado] método __converter: {e}")
        return None