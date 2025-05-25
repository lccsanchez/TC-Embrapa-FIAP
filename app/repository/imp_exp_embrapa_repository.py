"""
Repositório para operações de ImportacaoExportacao a partir de ETL Embrapa.
"""
import uuid
from typing import List, Tuple
import pandas as pd
from unidecode import unidecode
from app.util import etl
from app.model.model import ImportacaoExportacao


def find_all(
    tipo_registro: type, tipo_operacao: str, url: str
) -> List[ImportacaoExportacao] | None:
    """Executa o ETL e converte os dados para objetos ImportacaoExportacao."""
    try:
        return __converter(tipo_registro, tipo_operacao, etl.execute(url))
    except Exception as exc:
        print(f"[Erro] método find_all: {exc}")
        return None


def __converter(
    tipo_registro: type,
    tipo_operacao: str,
    dataframes: List[Tuple[str, pd.DataFrame]],
) -> List[ImportacaoExportacao]:
    """Converte DataFrames em objetos ImportacaoExportacao."""
    items = []
    try:
        for classificacao, df in dataframes:
            df.columns = [unidecode(col.lower()) for col in df.columns]
            df = df.where(pd.notnull(df), None)
            ano_colunas = [
                col
                for col in df.columns
                if str(col).isdigit() and len(str(col)) == 4
            ]

            for _, row in df.iterrows():
                registro_anos = [
                    tipo_registro(
                        id=str(uuid.uuid4()),
                        ano=int(ano),
                        tipo_operacao=tipo_operacao,
                        quantidade=0 if not str(row[ano]).isdigit()
                        else (row[ano]),
                        valor=0 if not str(row[f"{ano}.1"]).isdigit()
                        else (row[f"{ano}.1"])
                    )
                    for ano in ano_colunas
                    if pd.notna(row[ano])
                ]
                pais_nome = row["pais"].strip()
                if registro_anos:
                    items.append(
                        ImportacaoExportacao(
                            id=str(uuid.uuid4()),
                            source_id=int(row["id"]),
                            pais=pais_nome,
                            classificacao=str.lower(classificacao),
                            registros_imp_exp=registro_anos,
                        )
                    )

        return items

    except (ValueError, KeyError) as exc:
        print(f"[Erro de Dados] Verifique a estrutura do DataFrame: {exc}")
        return None
    except Exception as exc:
        print(f"[Erro Inesperado] método __converter: {exc}")
        return None
