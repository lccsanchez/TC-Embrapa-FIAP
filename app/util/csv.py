import pandas as pd
import requests
import os
from io import StringIO
from app.util import reader


def read(url, timeout): 
    try:
        text= reader.read(url, timeout)
         
        data = StringIO(text)

        separator = detect_separator(text)
        
        return pd.read_csv(data,sep=separator , encoding="utf-8" )

    except (UnicodeDecodeError, requests.RequestException) as e:
        raise ValueError(f"Não foi possível ler a URL {url}", {e})


def read_local(key: str) -> pd.DataFrame:
    
    # Processa o arquivo local
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    resultado = os.path.join(base_dir, "app", "data", f"{key}.csv")
    print(f"Processando arquivo local: {resultado}")
    with open(resultado, "r", encoding="utf-8") as file:
        file_content = file.read()

    # Detecta o separador automaticamente, se necessário
    sep = detect_separator(file_content) 

    # Carrega o conteúdo do arquivo local em um DataFrame
    return pd.read_csv(StringIO(file_content), sep=sep, encoding="utf-8")
    
def detect_separator(file_content: str) -> str: ## ok
   
    first_lines = [
        line for line in file_content.splitlines()[:5]
    ]

    commas = sum(line.count(",") for line in first_lines)
    tabs = sum(line.count("\t") for line in first_lines)
    semicolons = sum(line.count(";") for line in first_lines)

    if commas > tabs and commas > semicolons:
        return ","
    elif tabs > commas and tabs > semicolons:
        return "\t"
    else:
        return ";"
