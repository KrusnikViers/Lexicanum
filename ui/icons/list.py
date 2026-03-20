from enum import Enum
from pathlib import Path

from PySide6.QtGui import QIcon


def _load_icon(name: str) -> QIcon:
    icon_path = Path(__file__).parent / name
    if not icon_path.is_file():
        raise FileNotFoundError(f"{str(icon_path)} does not exist or is not a file.")
    return QIcon(str(icon_path))


class IconsList(Enum):
    # Adding icons: ICON_NAME = _load_icon('icon.svg')
    pass
