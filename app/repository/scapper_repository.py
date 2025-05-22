from app.util.scrapping.strategy_just_item import JustItems
from app.util.scrapping.strategy_with_subitems import WithSubItems
import app.urls_scrapping as urls
from app.util import reader


def find_with_subitems(year: str,opcao, subopcao=None):
    try:

        content = __get_content(year,opcao,subopcao)
        
        return WithSubItems().scrape(content)

    except (Exception) as e:
        print(f"[find_by_year] Não foi possivel realizar o scrapping: {e}")
        return None
    
def find_with_justitems(year: str,opcao, subopcao=None):
    try:
        
        content = __get_content(year,opcao,subopcao)
        
        return JustItems().scrape(content)

    except (Exception) as e:
        print(f"[find_by_year] Não foi possivel realizar o scrapping: {e}")
        return None
    
def __get_content(year: str,opcao, subopcao=None):
     cod_opcao = urls.sessions[opcao]["item"]
     cod_sub_opcao =  urls.sessions[opcao]["sub"].get(subopcao) if subopcao else None
     url = urls.get_url_scrapping (year,cod_opcao,cod_sub_opcao)
     return reader.read(url) 