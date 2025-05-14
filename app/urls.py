# Construir todas urls da página

# Chaves para formação das páginas com diferentes detalhamentos
itens_processamento = ['ProcessaViniferas','ProcessaAmericanas', 'ProcessaMesa', 'ProcessaSemclass']
itens_importacao = ['ImpVinhos', 'ImpEspumantes', 'ImpFrescas', 'ImpPassas', 'ImpSuco']
itens_exportacao = ['ExpVinho','ExpEspumantes', 'ExpUva', 'ExpSuco']
itens_comercializacao = ['Comercio']
itens_producao = ['Producao']

# Urls de todas as páginas que possuem arquivos para download
url_base = 'http://vitibrasil.cnpuv.embrapa.br/download'

url_producao = {
    
  item: f'{url_base}/{item}.csv'  
  for item in itens_producao

}
separador_producao = ";"

urls_processamento = {
  item: f'{url_base}/{item}.csv'  
  for item in itens_processamento
}
separador_processamento = ";"

url_comercializacao = {
  item: f'{url_base}/index.php?opcao=opt_04'
  for item in itens_comercializacao
}

urls_importacao = {
  item: f'{url_base}/index.php?subopcao=subopt_0{i}&opcao=opt_05'
  for i, item in zip(range(1,6), itens_importacao)
}

urls_exportacao = {
  item: f'{url_base}/index.php?subopcao=subopt_0{i}&opcao=opt_06'
  for i, item in zip(range(1,5), itens_exportacao)
}