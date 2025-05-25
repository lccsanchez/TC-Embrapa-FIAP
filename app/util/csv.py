"""Funções utilitárias para leitura e detecção de CSV."""

import os
from io import StringIO
import pandas as pd
import requests
from app.util import reader


def read(url, timeout):
    """Lê um arquivo CSV de uma URL."""
    try:
        text = reader.read(url, timeout)
        data = StringIO(text)
        separator = detect_separator(text)
        return pd.read_csv(data, sep=separator, encoding="utf-8")
    except (UnicodeDecodeError, requests.RequestException) as e:
        raise ValueError(f"Não foi possível ler a URL {url}", {e}) from e


def read_local(key: str) -> pd.DataFrame:
    """Lê um arquivo CSV local pelo nome da chave."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    resultado = os.path.join(base_dir, "app", "data", f"{key}.csv")
    print(f"Processando arquivo local: {resultado}")
    with open(resultado, "r", encoding="utf-8") as file:
        file_content = file.read()
    sep = detect_separator(file_content)
    return pd.read_csv(StringIO(file_content), sep=sep, encoding="utf-8")


def detect_separator(file_content: str) -> str:
    """Detecta o separador de um arquivo CSV."""
    first_lines = list(file_content.splitlines()[:5])

    commas = sum(line.count(",") for line in first_lines)
    tabs = sum(line.count("\t") for line in first_lines)
    semicolons = sum(line.count(";") for line in first_lines)

    if commas > tabs and commas > semicolons:
        return ","
    if tabs > commas and tabs > semicolons:
        return "\t"
    return ";"
