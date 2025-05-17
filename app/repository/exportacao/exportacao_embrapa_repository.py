from typing import List, Tuple
import pandas as pd

from app.urls import urls_exportacao, separador_exportacao
from app.util import collections, etl
from app.dto import ExportacaoDto, RegistrosImpExpDto


def find_all() -> List[ExportacaoDto] | None:
    try:
        return etl.execute(urls_exportacao, separador_exportacao, __converter)
    except Exception as e:
        print(f"[Erro] método find_all: {e}")
        return None


def find_by_year(year: int, classificacao: str) -> List[ExportacaoDto] | None:
    try:
        data = etl.execute(urls_exportacao, separador_exportacao, __converter)

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


def __converter(dataframes: List[Tuple[str, pd.DataFrame]]) -> List[ExportacaoDto]:

    exportacoes = []

    try:
        for key, df in dataframes:
            ano_colunas = [
                col for col in df.columns if str(col).isdigit() and len(str(col)) == 4
            ]
            classification = key

            for _, row in df.iterrows():
                exportacao_anos = [
                    RegistrosImpExpDto(
                        ano=ano,
                        quantidade=0 if not str(row[ano]).isdigit() else (row[ano]),
                        valor=0 if not str(row[f"{ano}.1"]).isdigit() else (row[f"{ano}.1"])
                    )
                    for ano in ano_colunas
                    if pd.notna(row[ano])
                ]

                if exportacao_anos:
                    exportacoes.append(
                        ExportacaoDto(
                            id=str(row["Id"]),
                            pais=row["País"],
                            classificacao=(
                                "" if classification is None else classification
                            ),
                            registros=exportacao_anos,
                        )
                    )

        return exportacoes

    except (ValueError, KeyError) as e:
        print(f"[Erro de Dados] Verifique a estrutura do DataFrame: {e}")
        return None
    except Exception as e:
        print(f"[Erro Inesperado] método __converter: {e}")
        return None
