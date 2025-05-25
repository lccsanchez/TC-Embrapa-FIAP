"""Estratégia para scraping de itens simples."""

from bs4 import BeautifulSoup


class JustItems():
    """Estratégia para o scraping do tipo 2."""

    def scrape(self, html_content: str):
        """Realiza o scraping de itens simples."""
        soup = BeautifulSoup(html_content, "html.parser")
        items = soup.find(class_="tb_base tb_dados")
        results = {}
        if not items:
            return results

        for item in items.find_all("tr"):
            data = item.find_all("td")
            if len(data) >= 3:
                pais = data[0].text.strip()
                results[pais] = {
                    "Quantidade": data[1].text.strip(),
                    "Valor": data[2].text.strip(),
                }
        return results
