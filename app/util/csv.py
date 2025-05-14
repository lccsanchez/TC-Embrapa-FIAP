import pandas as pd
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import os
from io import StringIO

def read(url, timeout=30):       

    proxies = {
   ##"http": "http://156.233.87.213:3129",
    "http": "http://e77bec8c:mshlekabsl9s@proxy.toolip.io:31111"
    }
    try:
        response = requests.get(url, timeout=timeout, verify=False)#, proxies=proxies)
        response.raise_for_status()  # Verifica erros HTTP
        data = StringIO(response.text)
        separator = detect_separator(response.text)
        return pd.read_csv(data,sep=separator , encoding="utf-8" )

    except (UnicodeDecodeError, requests.RequestException) as e:
        raise ValueError(f"Não foi possível ler a URL {url}", {e})


def read_local(key: str, separator: str) -> pd.DataFrame:
    
    # Processa o arquivo local
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    resultado = os.path.join(base_dir, "app", "data", f"{key}.csv")
    print(f"Processando arquivo local: {resultado}")
    with open(resultado, "r", encoding="utf-8") as file:
        file_content = file.read()

    # Detecta o separador automaticamente, se necessário
    sep = detect_separator(file_content) if not separator else separator

    # Carrega o conteúdo do arquivo local em um DataFrame
    return pd.read_csv(StringIO(file_content), sep=sep, encoding="utf-8")
    


def __load(url: str,separator: str, key: str) -> pd.DataFrame:

    print(f'A url final é {url}')

    if url is None:        
        print(f"Erro ao buscar o CSV para {url}.")
        return None

    try:
        csv_dataframe = csv.read(url)

        print(f'CSV carregado com sucesso: {url}')

        return csv_dataframe

    except Exception as e:
        print(f"Erro ao transformar {url}: {e}")
        print("Tentando carregar o arquivo local...")

        try:
            # Processa o arquivo local
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            resultado = os.path.join(base_dir,"app","data", f"{key}.csv")
            print(f"Processando arquivo local: {resultado}")
            with open(resultado, "r", encoding="utf-8") as file:
                file_content = file.read()

            # Detecta o separador automaticamente, se necessário
            sep = detect_separator(file_content) if not separator else separator

            # Carrega o conteúdo do arquivo local em um DataFrame
            csv_data = pd.read_csv(
                StringIO(file_content), sep=sep, encoding="utf-8"
            )
            print(f"Arquivo local carregado com sucesso: {resultado}")
            return csv_data

        except Exception as e:
            print(f"Erro ao carregar o arquivo local: {e}")
            return None


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
