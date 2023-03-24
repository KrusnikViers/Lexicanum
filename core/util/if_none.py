from typing import TypeVar

_T = TypeVar('_T')


def if_none(value: _T | None, default: _T) -> _T:
    if value is None:
        return default
    return value
