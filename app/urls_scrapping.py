#URLS para scraping de dados direto do site da Embrapa

from prefix import prefix

def get_url_scrapping(ano: str, cod_opcao: str, cod_subopcao: str = None):
    return f"http://{prefix.valor}vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={cod_opcao}" if cod_subopcao is None else f"http://{prefix.valor}vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={cod_opcao}&subopcao={cod_subopcao}"

sessions = {
    "producao": {"item": "opt_02"},
    "processamento": { 
        "item": "opt_03",
        "sub": {
            "ProcessaViniferas": "subopt_01",
            "ProcessaAmericanas": "subopt_02",
            "ProcessaMesa": "subopt_03",
            "ProcessaSemclass": "subopt_04",
        }
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
        }
    },
    "exportacao": {
        "item": "opt_06",
        "sub": {
            "ExpVinho": "subopt_01",
            "ExpEspumantes": "subopt_02",
            "ExpUva": "subopt_03",
            "ExpSuco": "subopt_04",
        },
    }
}