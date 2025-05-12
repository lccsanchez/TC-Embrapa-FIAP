from typing import List, Callable, TypeVar

T = TypeVar('T')

def filter(data: List[T], predicate: Callable[[T], bool]) -> List[T]:
    try:
        return [item for item in data if predicate(item)]
    except Exception as e:
        print(f"[Erro] método generic_filter: {e}")
        return []