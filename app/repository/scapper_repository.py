"""Repositório para scraping de dados do site da Embrapa."""

from app.util.scrapping.strategy_just_item import JustItems
from app.util.scrapping.strategy_with_subitems import WithSubItems
import app.util.url.urls_scrapping as urls
from app.util import reader


def find_with_subitems(year: str, opcao, subopcao=None):
    """Busca dados com subitens via scraping."""
    try:
        content = __get_content(year, opcao, subopcao)
        return WithSubItems().scrape(content)
    except ValueError as exc:
        raise exc
    except Exception as exc:
        print(f"[find_by_year] Não foi possivel realizar o scrapping: {exc}")
        return None


def find_with_justitems(year: str, opcao, subopcao=None):
    """Busca dados sem subitens via scraping."""
    try:
        content = __get_content(year, opcao, subopcao)
        return JustItems().scrape(content)
    except Exception as exc:
        print(f"[find_by_year] Não foi possivel realizar o scrapping: {exc}")
        return None


def __get_content(year: str, opcao, subopcao=None):
    """Obtém o conteúdo HTML para scraping."""
    cod_opcao = urls.sessions[opcao]["item"]

    if not cod_opcao:
        raise ValueError(f"Opção informada é invalida : {opcao}")

    cod_sub_opcao = urls.sessions[opcao]["sub"].get(subopcao) if subopcao else None

    if not cod_sub_opcao and str.rstrip(str.lstrip(opcao)) == "processamento":
        raise ValueError(f"Subopcao informada é invalida : {subopcao}")

    url = urls.get_url_scrapping(year, cod_opcao, cod_sub_opcao)
    return reader.read(url)
