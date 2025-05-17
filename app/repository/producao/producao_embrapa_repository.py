import uuid
from typing import List,Tuple
import pandas as pd

from urls import url_producao
from app.util import etl
from model.entidades import Produto, RegistroProducao 


def find_all() -> List[Produto] | None:   
    try:
        return etl.execute(url_producao, __converter)
    except Exception as e:
        print(f"[Erro] método find_all: {e}")
        return None

def __converter(dataframes: List[Tuple[str, pd.DataFrame]]) -> List[Produto]:

    producoes = []

    try:
        for _, df in dataframes:          
            ano_colunas = [col for col in df.columns if str(col).isdigit() and len(str(col)) == 4]

            for _, row in df.iterrows():              
                producao_anos = [
                    RegistroProducao(
                        id=str(uuid.uuid4()),                          
                        tipo_operacao='producao',
                        ano=int(ano), 
                        quantidade = 0 if not str(row[ano]).isdigit() else (row[ano])
                    )
                    for ano in ano_colunas
                    if pd.notna(row[ano])
                ]

                if producao_anos:
                    producoes.append(Produto(
                        id=str(uuid.uuid4()),
                        source_id =int(row['id']),
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