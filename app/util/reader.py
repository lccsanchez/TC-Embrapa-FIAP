"""Função utilitária para leitura de conteúdo de URL."""

import requests


def read(url, timeout=10):
    """Lê o conteúdo de uma URL e retorna como texto."""
    response = requests.get(url, timeout=timeout)
    response.encoding = "utf8"
    response.raise_for_status()
    return response.text
