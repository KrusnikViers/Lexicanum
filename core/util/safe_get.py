from typing import List, TypeVar

_T = TypeVar('_T')


def safe_get(container: List[_T] | str, index: int, default: _T | None = None) -> _T | None:
    try:
        return container[index]
    except IndexError:
        return default
