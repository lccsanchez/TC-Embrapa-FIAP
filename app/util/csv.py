import pandas as pd
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from io import StringIO

def read(url, timeout=30): 
   
   
    try:
        response = requests.get(url, timeout=(10, 30), verify=False)
        response.raise_for_status()  # Verifica erros HTTP
        data = StringIO(response.text)
        separator = detect_separator(response.text)
        return pd.read_csv(data,sep=separator , encoding="utf-8" )
        
    except (UnicodeDecodeError, requests.RequestException) as e:
           raise ValueError(f"Não foi possível ler a URL {url}", {e})


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
