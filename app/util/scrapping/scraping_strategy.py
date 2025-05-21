from abc import ABC, abstractmethod
 
class ScrapingStrategy(ABC):
    """Interface para estratégias de scraping."""

    @abstractmethod
    def scrape(self, html_content: str):
        pass
