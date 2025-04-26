from bs4 import BeautifulSoup
from io import StringIO
import json
import pandas as pd
import requests
import urls


def detect_separator(file_content: str):
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


def buscar_csv(url: str):
    """
    Busca o link de um arquivo CSV em uma página web e retorna a URL completa do arquivo.
    Args:
        url (str): A URL da página web onde o arquivo CSV será procurado.
    Returns:
        str: A URL completa do arquivo CSV, caso encontrado.
    Raises:
        requests.exceptions.RequestException: Se ocorrer um erro na requisição HTTP.
        requests.exceptions.HTTPError: Se a resposta HTTP indicar um erro.
    Nota:
        Caso nenhum arquivo CSV seja encontrado na página, a função imprime uma mensagem
        informando que o CSV não foi encontrado e retorna None.
    """

    response = requests.get(url, timeout=5)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    link_csv_tag = soup.find("a", href=lambda x: x and x.endswith(".csv"))

    if link_csv_tag:
        link_csv = link_csv_tag["href"]
        url_base = url.rsplit("/", 1)[0]
        url_full = f"{url_base}/{link_csv}"
        return url_full
    else:
        print(f"CSV não encontrado na página: {url}")


def processar_dados(url: str):
    """
    Retorna um pd.DataFrame processado de um arquivo obtido a partir de uma URL.

    Args:
        url (str): URL base para buscar o arquivo CSV.

    Returns:
        pd.DataFrame: DataFrame processado contendo as colunas 'classificacao', 
                      'categoria', 'cultivar', 'ano' e 'quantidade(kg)'.
                      Retorna None se a URL não for válida ou se ocorrer um erro.

    Raises:
        Exception: Caso ocorra algum erro durante o processamento do arquivo CSV.
    """

    url_full = buscar_csv(url)
    if not url_full:
        return None

    try:
        response = requests.get(url_full)
        response.raise_for_status()
        file_content = response.text

        sep = detect_separator(file_content)
        csv_data = pd.read_csv(
            StringIO(file_content), sep=sep, encoding="utf-8", index_col="id"
        )

        # Remover linhas de agrupamento
        linhas_remover = ["TINTAS", "BRANCASEROSADAS", "BRANCAS"]
        csv_data = csv_data[~csv_data["control"].isin(linhas_remover)].reset_index(
            drop=True
        )

        # Separação da coluna control em categoria e exclusão da coluna control
        csv_data["categoria"] = csv_data["control"].str.split("_").str[0]
        csv_novo = csv_data.drop(columns=["control"])

        # Detectar a classificação com base no nome do arquivo e incluir na nova coluna classificacao
        url_arquivo = url_full.lower()
        if "americanas" in url_arquivo:
            classificacao = "Americanas"
        elif "mesa" in url_arquivo:
            classificacao = "Mesa"
        elif "semclass" in url_arquivo:
            classificacao = "SemClass"
        elif "viniferas" in url_arquivo:
            classificacao = "Viniferas"
        else:
            classificacao = "Desconhecida"

        csv_novo["classificacao"] = classificacao

        # Transpor Colunas de anos em linhas mantendo as colunas classificacao, categoria e cultivar
        csv_data_melted = csv_novo.melt(
            id_vars=["classificacao", "categoria", "cultivar"],
            var_name="ano",
            value_name="quantidade(kg)",
        )

        return csv_data_melted

    except Exception as e:
        print(f"Erro ao processar {url_full}: {e}")
        return None


def agrupar_dados(urls_dict: dict):
    """
    Agrupa dados processados a partir de URLs fornecidas em um único DataFrame.

    Args:
        urls_dict (dict): Um dicionário onde as chaves são identificadores e os valores são URLs contendo os dados a serem processados.

    Returns:
        pandas.DataFrame: Um DataFrame contendo os dados agrupados de todas as URLs processadas.

    Raises:
        ValueError: Se o dicionário fornecido estiver vazio ou se nenhum dado válido for processado.
        Exception: Para outros erros inesperados durante o processamento dos dados.
    """

    arquivos_csv = []
    for url in urls_dict.values():
        dados = processar_dados(url)
        if dados is not None:
            arquivos_csv.append(dados)

    dados_agrupados = pd.concat(arquivos_csv, ignore_index=True)

    return dados_agrupados


def gerar_json_agrupado(url):

    """
    Gera uma estrutura JSON agrupada a partir de dados obtidos de uma URL.
    Utiliza a função `agrupar_dados` para processar os dados e organizá-los em uma hierarquia.
    A função organiza os dados em uma hierarquia baseada em classificação, ano, categoria 
    e cultivares, retornando uma estrutura JSON agrupada e ordenada.

    Args:
        url (str): URL contendo os dados a serem agrupados.

    Returns:
        dict: Estrutura JSON agrupada e ordenada com os seguintes níveis:
            - Classificação: Agrupamento principal.
            - Ano: Subagrupamento dentro de cada classificação.
            - Categoria: Subagrupamento dentro de cada ano.
            - Cultivares: Lista de cultivares com suas respectivas quantidades.

    Raises:
        ValueError: Se os dados obtidos da URL não estiverem no formato esperado.
        Exception: Para outros erros que possam ocorrer durante o processamento dos dados.
    """

    dados_agrupados = agrupar_dados(url)

    estrutura_final = {}

    # Agrupando os dados por classificação
    for classificacao, df_class in dados_agrupados.groupby("classificacao"):
        anos_list = []

        # Agrupando os dados por ano dentro de cada classificação
        for ano, df_ano in df_class.groupby("ano"):
            categorias_list = []

            # Agrupando os dados por categoria dentro de cada ano
            for categoria, df_categoria in df_ano.groupby("categoria"):
                cultivares_list = []

                # Iterando sobre as linhas de cada categoria para montar a lista de cultivares
                for _, linha in df_categoria.iterrows():
                    cultivares_list.append(
                        {
                            "cultivar": linha["cultivar"],
                            "quantidade(kg)": linha["quantidade(kg)"],
                        }
                    )

                # Adicionando a categoria com a lista de cultivares à lista de categorias
                categorias_list.append(
                    {"categoria": categoria, "cultivares": cultivares_list}
                )

            # Ordenando as categorias por nome
            categorias_list = sorted(categorias_list, key=lambda x: x["categoria"])

            # Adicionando o ano com a lista de categorias à lista de anos
            anos_list.append(
                {
                    "ano": str(ano),  # Convertendo o ano para string
                    "categorias": categorias_list,
                }
            )

        # Ordenando os anos por ordem crescente
        anos_list = sorted(anos_list, key=lambda x: int(x["ano"]))

        # Adicionando a classificação com a lista de anos à estrutura final
        estrutura_final[classificacao] = anos_list

    return estrutura_final


# Opcional: imprimir JSON formatado
json_formatado = json.dumps(
    gerar_json_agrupado(urls.urls_processamento), ensure_ascii=False, indent=2
)
