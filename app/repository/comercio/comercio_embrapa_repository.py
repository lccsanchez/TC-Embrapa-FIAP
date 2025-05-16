from typing import List,Tuple
import pandas as pd

from urls import url_comercializacao, separador_comercializacao
from app.util import collections, etl
from dto import ComercioDto, RegistrosDto 


def find_all() -> List[ComercioDto] | None:   
    try:
        return etl.execute(url_comercializacao, separador_comercializacao, __converter)
    except Exception as e:
        print(f"[Erro] método find_all: {e}")
        return None


def find_by_year(year: int) -> List[ComercioDto] | None:
    try:
        data = etl.execute(url_comercializacao, separador_comercializacao, __converter)

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

def __converter(dataframes: List[Tuple[str, pd.DataFrame]]) -> List[ComercioDto]:

    comercios = []

    try:
        for _, df in dataframes:          
            ano_colunas = [col for col in df.columns if str(col).isdigit() and len(str(col)) == 4]

            for _, row in df.iterrows():              
                comercio_anos = [
                    RegistrosDto(ano=ano, quantidade = 0 if not str(row[ano]).isdigit() else (row[ano]))
                    for ano in ano_colunas
                    if pd.notna(row[ano])
                ]

                if comercio_anos:
                    comercios.append(
                        ComercioDto(
                            id=str(row["id"]),
                            control=(
                                row["Produto"]
                                if not row["control"] or str(row["control"]).strip()
                                else row["control"]
                            ),
                            produto=row["Produto"],
                            registros=comercio_anos,
                        )
                    )

        return comercios

    except (ValueError, KeyError) as e:
        print(f"[Erro de Dados] Verifique a estrutura do DataFrame: {e}")
        return None
    except Exception as e:
        print(f"[Erro Inesperado] método __converter: {e}")
        return None
