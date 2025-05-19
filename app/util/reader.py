import requests
from io import StringIO

def read(url, timeout=10): 
    try:
        response = requests.get(url, timeout=timeout)
        response.encoding = "utf8"
        response.raise_for_status()   
               
        return response.text
    except (Exception) as e:
        raise ValueError(f"Não foi possível ler a URL {url}", {e})