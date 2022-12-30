from typing import TypeVar

_T = TypeVar('_T')


def if_none(value: _T | None, default: _T) -> _T:
    assert default is not None, "This call is no-op for |None| as a default value"
    if value is None:
        return default
    return value
