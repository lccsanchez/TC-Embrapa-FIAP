import requests
from io import StringIO

def read(url, timeout=10): 
    
    response = requests.get(url, timeout=timeout)
    response.encoding = "utf8"
    response.raise_for_status()   
            
    return response.text
     