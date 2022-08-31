from typing import TypeVar, Optional, Any, Generic

_T = TypeVar('_T')


class StatusOr(Generic[_T]):
    def __init__(self, value: Optional[_T] = None, status: Optional[str] = None):
        assert (value is None) != (status is None)
        self.value: Optional[_T] = value
        self.status: Optional[str] = status

    def is_ok(self) -> bool:
        return self.value is not None

    @staticmethod
    def from_status(status: str) -> 'StatusOr':
        return StatusOr(status=status)

    @staticmethod
    def from_value(value: Any) -> 'StatusOr':
        return StatusOr(value=value)
