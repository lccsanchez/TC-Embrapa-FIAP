"""Funções utilitárias para ETL de dados."""

from typing import TypeVar

import pandas as pd

from app.util import csv

T = TypeVar("T")


def _load(url: str, key=None) -> pd.DataFrame:
    """Carrega um DataFrame a partir de uma URL."""
    print(f"A url final é {url}")

    if url is None:
        print(f"Erro ao buscar o CSV para {url}.")
        return None

    try:
        csv_dataframe = csv.read(url, 10)
        print(f"CSV carregado com sucesso: {url}")
        return csv_dataframe

    except Exception as e:
        print(f"Erro ao transformar {url}: {e}")
        return None


def execute(url_dict):
    """Executa o ETL para um dicionário de URLs."""
    if not isinstance(url_dict, dict):
        raise TypeError("url_dict deve ser um dicionário")
    result = []
    for key, url in url_dict.items():
        if url is None:
            return None
        try:
            df = _load(url, key)
        except Exception:
            return None
        if df is None or getattr(df, "empty", True):
            return None
        result.append((key, df))
    return result
