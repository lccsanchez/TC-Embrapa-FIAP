from bs4 import BeautifulSoup
from io import StringIO
import json
import pandas as pd
import requests
import os

def detect_separator(file_content: str) -> str:
    """
    Detecta o separador predominante em um conteúdo de arquivo fornecido.
    Esta função analisa as primeiras 5 linhas do conteúdo do arquivo e conta 
    a ocorrência de três tipos de separadores: vírgulas (","), tabulações ("\t") 
    e ponto e vírgula (";"). O separador com maior número de ocorrências é retornado.

    Args:
        file_content (str): O conteúdo do arquivo como uma string.

    Returns:
        str: O separador predominante, que pode ser uma vírgula (","), 
             uma tabulação ("\t") ou um ponto e vírgula (";").
    """

    first_lines = [
        line for line in file_content.splitlines()[:5]
    ]

    commas = sum(line.count(",") for line in first_lines)
    tabs = sum(line.count("\t") for line in first_lines)
    semicolons = sum(line.count(";") for line in first_lines)

    if commas > tabs and commas > semicolons:
        return ","
    elif tabs > commas and tabs > semicolons:
        return "\t"
    else:
        return ";"

def buscar_csv(url: str, key: str) -> str:
    """
    Busca um arquivo CSV em uma página web ou retorna um arquivo local caso o download falhe.
    Args:
        url (str): A URL da página web onde o arquivo CSV deve ser procurado.
        key (str): Uma chave identificadora usada para localizar o arquivo CSV localmente, 
                   caso o download falhe.
    Returns:
        str: O caminho completo para o arquivo CSV encontrado na web ou localmente. 
             Retorna `None` se o arquivo não for encontrado em ambos os casos.
    Comportamento:
        - Faz uma requisição HTTP para a URL fornecida e tenta localizar um link para um arquivo CSV.
        - Se o link for encontrado, retorna a URL completa do arquivo CSV.
        - Caso ocorra um erro na requisição ou o arquivo CSV não seja encontrado na página, 
          tenta retornar o caminho de um arquivo local na pasta 'data' com o nome baseado na chave fornecida.
        - Exibe mensagens no console para indicar o progresso e possíveis erros.
    """

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        link_csv_tag = soup.find("a", href=lambda x: x and x.endswith(".csv"))

        if link_csv_tag:
            link_csv = link_csv_tag["href"]
            url_base = url.rsplit("/", 1)[0]
            url_full = f"{url_base}/{link_csv}"
            print('Retornando URL completa:', url_full)
            return url_full
        else:
            print(f"CSV não encontrado na página: {url}")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")

        # Tentar retornar o arquivo local na pasta 'data' (uso para processamento dos dados)
        local_file_path = os.path.join("data", f"{key}.csv")
        if os.path.exists(local_file_path):
            print(f"Retornando arquivo local: {local_file_path}")
            return local_file_path
        else:
            print(f"Arquivo local não encontrado: {local_file_path}")
            return None

def processar_operacao(df: pd.DataFrame, url: str) -> pd.DataFrame:
    """
    Processa um DataFrame contendo informações de produtos de Processamento,
    Produção e Comercialização e retorna um DataFrame transformado.
    Esta função realiza as seguintes operações:

    Args:
        df (pd.DataFrame): DataFrame de entrada contendo os dados a serem processados.
        url (str): URL ou caminho do arquivo que será usado para determinar a classificação.
    Returns:
        pd.DataFrame: DataFrame transformado com as colunas 
        'classificacao' , 'categoria', 'produto', 'ano' e 'quantidade'.
    """


    df.columns = df.columns.str.lower()

    # Renomear a coluna 'cultivar' para 'produto', se existir
    if "cultivar" in df.columns:
        df.rename(columns={"cultivar": "produto"}, inplace=True)

    # Remover linhas de agrupamento
    df = df[~((df["control"] == df["produto"]) 
            | (df["control"].isna())
            | (df["control"] == "BRANCASEROSADAS")
        )].reset_index(drop=True)

    # Separação da coluna control em categoria e exclusão da coluna control
    df["categoria"] = df["control"].str.split("_").str[0]
    df_novo = df.drop(columns=["control"])

    # Detectar a classificação com base no nome do arquivo e incluir na nova coluna classificacao
    url_arquivo = url.lower()
    if "americanas" in url_arquivo:
        classificacao = "Americanas"
    elif "mesa" in url_arquivo:
        classificacao = "Mesa"
    elif "semclass" in url_arquivo:
        classificacao = "SemClass"
    elif "viniferas" in url_arquivo:
        classificacao = "Viniferas"
    else:
        classificacao = "" # Comercializacao e Produção não possuem classificação definida

    df_novo["classificacao"] = classificacao

    # Transpor Colunas de anos em linhas mantendo as colunas classificacao, categoria e produto
    df_melted = df_novo.melt(
        id_vars=["classificacao", "categoria", "produto"],
        var_name="ano",
        value_name="quantidade",
    )

    return df_melted

def processar_dados(url: str, key: str) -> pd.DataFrame:
    """
    Processa os dados de um arquivo CSV, seja ele remoto ou local, e retorna um DataFrame processado.
    Args:
        url (str): URL ou caminho local para buscar o arquivo CSV.
        key (str): Chave identificadora para o arquivo, usada para salvar localmente (se necessário).
    Returns:
        pd.DataFrame: DataFrame processado com os dados do CSV.
                      Retorna None se ocorrer algum erro durante o processamento.
    Comportamento:
        - Busca o arquivo CSV utilizando a função `buscar_csv`.
        - Verifica se o arquivo é remoto (URL) ou local e realiza o processamento adequado.
        - Detecta automaticamente o separador do arquivo CSV.
        - Lê o conteúdo do arquivo CSV em um DataFrame.
        - Processa o DataFrame utilizando a função `processar_operacao`.
        - Exibe mensagens de log para indicar o progresso e possíveis erros.
    Exceções:
        - Caso o arquivo não seja encontrado ou ocorra algum erro durante o processamento,
          uma mensagem de erro será exibida e a função retornará None.
    """

    resultado = buscar_csv(url, key)
    print(f'O resultado é {resultado}')

    if resultado is None:
        print(f"Erro ao buscar o CSV para {url}.")
        return None

    try:
        if resultado.startswith("http"):
            print(f'Processando arquivo remoto: {resultado}')
            response = requests.get(resultado, timeout=10)
            response.raise_for_status()
            file_content = response.text
            """ os.makedirs("data", exist_ok=True)  # Garante que a pasta 'data' exista
            local_file_path = os.path.join("data", f"{key}.csv")
            with open(local_file_path, "w", encoding="utf-8") as file:
                file.write(file_content)
            print(f"Arquivo CSV salvo em: {local_file_path}") """ #Pretendo utilizar para salvar o arquivo localmente
            

        else:
            print(f'Processando arquivo local: {resultado}')
            with open(resultado, "r", encoding="utf-8") as file:
                file_content = file.read()

        sep = detect_separator(file_content)

        csv_data = pd.read_csv(
            StringIO(file_content), sep=sep, encoding="utf-8", index_col="id"
        )

        # Utilizar if quando existir função para processar Importação e Exportação
        csv_data_melted = processar_operacao(csv_data, resultado) 

        print(f'CSV processado com sucesso: {resultado}')

        return csv_data_melted

    except Exception as e:
        print(f"Erro ao processar {resultado}: {e}")
        return None

def agrupar_dados(urls_dict: dict) -> pd.DataFrame:
    """
    Agrupa dados processados a partir de URLs fornecidas em um único DataFrame.
    Esta função recebe um dicionário contendo chaves e URLs, processa os dados
    de cada URL utilizando a função `processar_dados`, e concatena os DataFrames
    resultantes em um único DataFrame. Caso apenas um DataFrame seja gerado, ele
    é retornado diretamente. Se nenhum dado for processado, a função retorna `None`.
    Args:
        urls_dict (dict): Um dicionário onde as chaves representam identificadores
                          e os valores são URLs que apontam para os dados a serem processados.
    Returns:
        pd.DataFrame: Um DataFrame contendo os dados agrupados de todas as URLs processadas.
                      Retorna `None` se nenhum dado for processado.
    """

    arquivos_csv = []
    for key, url in urls_dict.items():
        print(f'Chave {key} URL: {url}')
        dados = processar_dados(url, key)
        if dados is not None:
            arquivos_csv.append(dados)

    # Verifica se há mais de um DataFrame para concatenar
    if len(arquivos_csv) > 1:
        dados_agrupados = pd.concat(arquivos_csv, ignore_index=True)
    elif len(arquivos_csv) == 1:
        dados_agrupados = arquivos_csv[0]  # Retorna o único DataFrame
    else:
        print("Nenhum dado foi processado.")
        return None

    return dados_agrupados

def gerar_json_hierarquico_operacoes(df: pd.DataFrame) -> dict:
    
    resultado = {}

    for _, row in df.iterrows():
        categoria = row["categoria"]
        produto = row["produto"]
        ano = row["ano"]
        quantidade = row["quantidade"]

        if "classificacao" in df.columns:
            classificacao = row["classificacao"]
            resultado.setdefault(classificacao, {}).setdefault(str(ano), {}).setdefault(categoria, {}).setdefault(produto, {})['quantidade'] = quantidade

        else:
            resultado.setdefault(str(ano), {}).setdefault(categoria, {}).setdefault(produto, {})['quantidade'] = quantidade

    return resultado

def filtrar_dados(df: pd.DataFrame, classificacao: str = None, ano: int = None, categoria: str = None) -> dict:
    
    df_filtrado = df.copy()

    if 'classificacao' in df_filtrado.columns and df_filtrado['classificacao'].nunique() <= 1:
        df_filtrado = df_filtrado.drop(columns=['classificacao'])

    if classificacao and 'classificacao' in df.columns:
        df_filtrado = df_filtrado[df_filtrado['classificacao'] == classificacao]
    if ano:
        df_filtrado = df_filtrado[df_filtrado['ano'] == int(ano)]
    if categoria:
        df_filtrado = df_filtrado[df_filtrado['categoria'] == categoria]

    if df_filtrado.empty:
        return {"message": "Nenhum dado encontrado para os filtros aplicados."}
    
    resultado = gerar_json_hierarquico_operacoes(df_filtrado)
    return resultado
