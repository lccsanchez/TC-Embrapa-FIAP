import uuid
from typing import List,Tuple
import pandas as pd
from app.util import etl
from app.model import Produto 


def find_all(tipo_registro: type,tipo_operacao: str, url: str) -> List[Produto] | None:   
    try:
        
        return __converter(tipo_registro,tipo_operacao,etl.execute(url))
    
    except Exception as e:
        print(f"[Erro] método find_all: {e}")
        return None


def __converter(tipo_registro: type, tipo_operacao: str, dataframes: List[Tuple[str, pd.DataFrame]]) -> List[Produto]:
    items = []

    try:
        for classificacao, df in dataframes:  
            df.columns = df.columns.str.lower()   
            df = df.where(pd.notnull(df), None)     
            ano_colunas = [col for col in df.columns if str(col).isdigit() and len(str(col)) == 4]

            for key, row in df.iterrows():              
                registro_anos = [
                    tipo_registro(
                        id=str(uuid.uuid4()),  
                        ano=int(ano), 
                        tipo_operacao=tipo_operacao,
                        quantidade = 0 if not str(row[ano]).isdigit() else (row[ano])
                    )
                    for ano in ano_colunas
                    if pd.notna(row[ano])
                ]
                produto_nome = (row['produto'] if "produto" in df.columns else row["cultivar"]).strip()
                control_name = (row['control'] if row['control'] else produto_nome).strip()
                if registro_anos:
                    items.append(Produto(
                        id=str(uuid.uuid4()),
                        source_id =int(row['id']),
                        control= control_name,
                        produto=produto_nome,
                        classificacao=str.lower(classificacao),
                        registros=registro_anos
                    ))             

        return items

    except (ValueError, KeyError) as e:
        print(f"[Erro de Dados] Verifique a estrutura do DataFrame: {e}")
        return None
    except Exception as e:
        print(f"[Erro Inesperado] método __converter: {e}")
        return None