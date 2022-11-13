from pathlib import Path

from PySide6.QtGui import QIcon


def _load_icon(name: str):
    icon_path = Path(__file__).parent / name
    assert icon_path.is_file()
    return QIcon(str(icon_path))


class SharedIcons:
    Search: QIcon = _load_icon('search.svg')
    Plus: QIcon = _load_icon('plus.svg')
    Trash: QIcon = _load_icon('trash.svg')
    Check: QIcon = _load_icon('check.svg')
    Sidebar: QIcon = _load_icon('sidebar.svg')
