from typing import List, TypeVar

_T = TypeVar('_T')


def safe_get(container: List[_T], index: int) -> _T | None:
    try:
        return container[index]
    except IndexError:
        return None
