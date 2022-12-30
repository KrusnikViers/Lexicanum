import copy
import pathlib


class UniversalPath:
    def __init__(self, str_path: str):
        self._path = pathlib.Path(str_path).resolve()

    def __str__(self):
        return self._path.as_posix()

    def with_extension(self, new_extension: str):
        new_self = copy.deepcopy(self)
        new_self._path = new_self._path.with_suffix(new_extension).resolve()
        return new_self

    def exists(self) -> bool:
        return self._path.exists()
