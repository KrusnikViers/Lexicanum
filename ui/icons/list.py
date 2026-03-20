from pathlib import Path

from PySide6.QtGui import QIcon


def _load_icon(relative_path: str) -> QIcon:
    icon_path = Path(__file__).parent / relative_path
    if not icon_path.is_file():
        raise FileNotFoundError(f"{str(icon_path)} does not exist or is not a file.")
    return QIcon(str(icon_path))

# Add icons below as ICON_NAME = _load_icon(relative_path).
