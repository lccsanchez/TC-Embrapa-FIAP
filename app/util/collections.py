"""Funções utilitárias para coleções."""

from typing import Callable, List, TypeVar

T = TypeVar("T")


def filter_collection(data: List[T], predicate: Callable[[T], bool]) -> List[T]:
    """Filtra uma lista usando o predicado informado."""
    try:
        return [item for item in data if predicate(item)]
    except Exception as exc:
        print(f"[Erro] método filter_collection: {exc}")
        return []
