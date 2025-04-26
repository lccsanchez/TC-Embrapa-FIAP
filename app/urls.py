# Construir todas urls da página

# Chaves para formação das páginas com diferentes detalhamentos
itens_processamento = ['Viniferas', 'Americanas', 'Mesa', 'SemClass']
itens_importacao = ['ImpVinhos', 'ImpEspumantes', 'ImpFrescas', 'ImpPassas', 'ImpSuco']
itens_exportacao = ['ExpVinho','ExpEspumantes', 'ExpUva', 'ExpSuco']

# Urls de todas as páginas que possuem arquivos para download
url_base = 'http://vitibrasil.cnpuv.embrapa.br'

url_producao = f'{url_base}/index.php?opcao=opt_02'

urls_processamento = {
  item: f'{url_base}/index.php?subopcao=subopt_0{i}&opcao=opt_03'
  for i, item in zip(range(1,5), itens_processamento)
}

url_comercializacao = f'{url_base}/index.php?opcao=opt_04'

urls_importacao = {
  item: f'{url_base}/index.php?subopcao=subopt_0{i}&opcao=opt_05'
  for i, item in zip(range(1,6), itens_importacao)
}

urls_exportacao = {
  item: f'{url_base}/index.php?subopcao=subopt_0{i}&opcao=opt_06'
  for i, item in zip(range(1,5), itens_exportacao)
}