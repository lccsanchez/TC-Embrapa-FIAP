"""Estratégia para scraping de itens com subitens."""

from bs4 import BeautifulSoup


class WithSubItems:
    """Estratégia para o scraping do tipo 1."""

    def scrape(self, html_content: str):
        """Realiza o scraping de itens com subitens."""
        empty_data = True
        soup = BeautifulSoup(html_content, "html.parser")
        items = soup.find(class_="tb_base tb_dados")
        results = {}
        item_name = None

        if not items:
            return results

        for item in items.find_all("tr"):
            data = item.find_all("td")
            if not data or len(data) < 2:
                continue
            if "tb_item" in data[0].get("class", []):
                item_name = data[0].get_text(strip=True)
                item_value = data[1].get_text(strip=True)
                if item_value != "-":
                    empty_data = False
                    results[item_name] = {"total": item_value, "subitems": []}
            elif "tb_subitem" in data[0].get("class", []) and item_name:
                subitem_name = data[0].get_text(strip=True)
                subitem_value = data[1].get_text(strip=True)
                results[item_name]["subitems"].append({subitem_name: subitem_value})
        return [] if empty_data else results
