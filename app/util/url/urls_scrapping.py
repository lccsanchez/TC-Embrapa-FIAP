"""URLs e sessões para scraping de dados do site da Embrapa."""

from app.util.url.gerenciamento_estado import estado


def get_url_scrapping(ano: str, cod_opcao: str, cod_subopcao: str = None):
    """Monta a URL para scraping de acordo com os parâmetros."""
    base_url = f"http://{estado.prefixo_url}" "vitibrasil.cnpuv.embrapa.br/index.php"
    if cod_subopcao is None:
        return f"{base_url}?ano={ano}&opcao={cod_opcao}"
    return f"{base_url}?ano={ano}&opcao={cod_opcao}" f"&subopcao={cod_subopcao}"


sessions = {
    "producao": {"item": "opt_02"},
    "processamento": {
        "item": "opt_03",
        "sub": {
            "ProcessaViniferas": "subopt_01",
            "ProcessaAmericanas": "subopt_02",
            "ProcessaMesa": "subopt_03",
            "ProcessaSemclass": "subopt_04",
        },
    },
    "comercio": {"item": "opt_04"},
    "importacao": {
        "item": "opt_05",
        "sub": {
            "ImpVinhos": "subopt_01",
            "ImpEspumantes": "subopt_02",
            "ImpFrescas": "subopt_03",
            "ImpPassas": "subopt_04",
            "ImpSuco": "subopt_05",
        },
    },
    "exportacao": {
        "item": "opt_06",
        "sub": {
            "ExpVinho": "subopt_01",
            "ExpEspumantes": "subopt_02",
            "ExpUva": "subopt_03",
            "ExpSuco": "subopt_04",
        },
    },
}
