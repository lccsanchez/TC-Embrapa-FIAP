"""URLs para download de arquivos de dados Embrapa."""

# Chaves para formação das páginas com diferentes detalhamentos
itens_processamento = [
    "ProcessaViniferas",
    "ProcessaAmericanas",
    "ProcessaMesa",
    "ProcessaSemclass",
]
itens_importacao = ["ImpVinhos", "ImpEspumantes", "ImpFrescas", "ImpPassas", "ImpSuco"]
itens_exportacao = ["ExpVinho", "ExpEspumantes", "ExpUva", "ExpSuco"]
itens_comercializacao = ["Comercio"]
itens_producao = ["Producao"]

URL_BASE = "http://vitibrasil.cnpuv.embrapa.br/download"

url_producao = {item: f"{URL_BASE}/{item}.csv" for item in itens_producao}

urls_processamento = {item: f"{URL_BASE}/{item}.csv" for item in itens_processamento}

url_comercializacao = {item: f"{URL_BASE}/{item}.csv" for item in itens_comercializacao}

urls_importacao = {item: f"{URL_BASE}/{item}.csv" for item in itens_importacao}

urls_exportacao = {item: f"{URL_BASE}/{item}.csv" for item in itens_exportacao}
