from typing import List, Tuple
import pandas as pd

from app.urls import urls_importacao, separador_importacao
from app.util import collections, etl
from app.dto import ImportacaoDto, RegistrosImpExpDto


def find_all() -> List[ImportacaoDto] | None:
    try:
        return etl.execute(urls_importacao, separador_importacao, __converter)
    except Exception as e:
        print(f"[Erro] método find_all: {e}")
        return None


def find_by_year(year: int, classificacao: str) -> List[ImportacaoDto] | None:
    try:
        data = etl.execute(urls_importacao, separador_importacao, __converter)

        if not data:
            return None

        for item in data:
            item.registros = collections.filter(
                item.registros, lambda p: int(p.ano) == int(year)
            )
        return data
    except Exception as e:
        print(f"[Erro] método find_by_year: {e}")
        return None


def __converter(dataframes: List[Tuple[str, pd.DataFrame]]) -> List[ImportacaoDto]:

    importacoes = []

    try:
        for key, df in dataframes:
            ano_colunas = [
                col for col in df.columns if str(col).isdigit() and len(str(col)) == 4
            ]
            classification = key

            for _, row in df.iterrows():
                importacao_anos = [
                    RegistrosImpExpDto(                        
                        ano=ano,
                        quantidade=0 if not str(row[ano]).isdigit() else (row[ano]),
                        valor=0 if not str(row[f"{ano}.1"]).isdigit() else (row[f"{ano}.1"])
                    )
                    for ano in ano_colunas
                    if pd.notna(row[ano])
                ]

                if importacao_anos:
                    importacoes.append(
                        ImportacaoDto(
                            id=str(row["Id"]),
                            pais=row["País"],
                            classificacao=(
                                "" if classification is None else classification
                            ),
                            registros=importacao_anos,
                        )
                    )

        return importacoes

    except (ValueError, KeyError) as e:
        print(f"[Erro de Dados] Verifique a estrutura do DataFrame: {e}")
        return None
    except Exception as e:
        print(f"[Erro Inesperado] método __converter: {e}")
        return None
