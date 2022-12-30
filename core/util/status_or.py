from typing import TypeVar, Generic

_T = TypeVar('_T')


class Status:
    def __init__(self, status: str | None = None):
        self.status: str | None = status

    def is_ok(self) -> bool:
        return self.status is None


class StatusOr(Generic[_T]):
    def __init__(self, value: _T | None = None, status: str | None = None):
        assert (value is None) != (status is None)
        self.value: _T | None = value
        self.status: str | None = status

    def is_ok(self) -> bool:
        return self.value is not None

    def to_pure(self) -> Status:
        assert not self.is_ok()
        return Status(self.status)

    def to_other(self) -> 'StatusOr':
        assert not self.is_ok()
        return StatusOr(status=self.status)
