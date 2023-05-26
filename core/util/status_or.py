from typing import TypeVar, Generic

_T = TypeVar('_T')


class Status:
    def __init__(self, status: str | None = None):
        self.status: str | None = status

    def __str__(self):
        return 'Status:OK' if self.is_ok() else 'Status:Err:{}'.format(self.status)

    def __bool__(self):
        return self.is_ok()

    def is_ok(self) -> bool:
        return self.status is None

    def is_error(self) -> bool:
        return self.status is not None


class StatusOr(Generic[_T]):
    def __init__(self, value: _T | None = None, status: str | None = None):
        assert (value is None) != (status is None)
        self.value: _T | None = value
        self.status: str | None = status

    def __str__(self):
        return 'StatusOr:OK:{}'.format(self.value) if self.is_ok() else 'StatusOr:Err:{}'.format(self.status)

    def __bool__(self):
        return self.is_ok()

    def is_ok(self) -> bool:
        return self.value is not None

    def is_error(self) -> bool:
        return self.status is not None

    def to_pure(self) -> Status:
        assert not self.is_ok()
        return Status(self.status)

    def to_other(self) -> 'StatusOr':
        assert not self.is_ok()
        return StatusOr(status=self.status)

    @classmethod
    def from_pure(cls, status: Status) -> 'StatusOr':
        assert not status.is_ok()
        return cls(status=status.status)
