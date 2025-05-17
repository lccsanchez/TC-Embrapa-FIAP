from util.scrapping.strategy_with_subitems import WithSubItems
import app.urls as urls
from util import reader

SECAO_PRODUCAO = "opt_02"

def find_by_year(year: str):
    try:

        url = urls.get_url_scrapping (year,SECAO_PRODUCAO)
        
        content = reader.read(url)
        
        return WithSubItems().scrape(content)

    except (Exception) as e:
        print(f"[find_by_year] Não foi possivel realizar o scrapping: {e}")
        return None
    
