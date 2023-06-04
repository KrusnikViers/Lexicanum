from pathlib import Path

from PySide6.QtGui import QIcon


def _load_icon(name: str):
    icon_path = Path(__file__).parent / name
    assert icon_path.is_file()
    return QIcon(str(icon_path))


class IconsList:
    New: QIcon = _load_icon('document.svg')
    Open: QIcon = _load_icon('folder-outline.svg')
    Save: QIcon = _load_icon('save-disk.svg')
    Export: QIcon = _load_icon('download.svg')
    Sidebar: QIcon = _load_icon('show-sidebar.svg')
