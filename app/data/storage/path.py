import pathlib


class Path:
    def __init__(self, str_path: str):
        self._path = pathlib.Path(str_path).resolve()

    def as_str(self):
        return self._path.as_posix()

    def with_suffix(self, suffix: str):
        return self._path.with_suffix(suffix).as_posix()

    def exists(self):
        return self._path.exists()
