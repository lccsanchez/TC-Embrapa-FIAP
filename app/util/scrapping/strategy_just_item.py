# pylint: disable=too-few-public-methods
"""Estratégia para scraping de itens simples."""

from bs4 import BeautifulSoup


class JustItems:
    """Estratégia para o scraping do tipo 2."""

    def scrape(self, html_content: str):
        empty_data = True
        """Realiza o scraping de itens simples."""
        soup = BeautifulSoup(html_content, "html.parser")
        items = soup.find(class_="tb_base tb_dados")
        empty_values = ["-","0"]
        results = {}
        if not items:
            return results

        for item in items.find_all("tr"):
            data = item.find_all("td")
            if len(data) >= 3:
                quantidade = data[1].text.strip()
                valor =data[2].text.strip()
                empty_data = False if not quantidade in empty_values or not valor in empty_values else True
                pais = data[0].text.strip()
                results[pais] = {
                    "Quantidade": quantidade,
                    "Valor": valor,
                }
               
        return [] if empty_data else results
