from collections import namedtuple
from enum import Enum

from PySide6.QtCore import QSettings, QRect

from app.info import PROJECT_NAME, PUBLISHER_NAME

_StoredSettingMeta = namedtuple('StoredSettingMeta', 'stored_name type default_value')


# Add new values to be stored in this enum.
class StoredSettings(Enum):
    LAST_PROJECT_FILE_PATH = _StoredSettingMeta('last_json_path', str, '')
    LAST_ANKI_FILE_PATH = _StoredSettingMeta('last_apkg_path', str, '')
    IMPORT_ON_STARTUP = _StoredSettingMeta('startup_autoimport', bool, True)
    MAIN_WINDOW_GEOMETRY = _StoredSettingMeta('main_window_geometry', QRect, QRect())
    SUMMARY_TABLE_COLUMNS_WIDTH_SPACED = _StoredSettingMeta('summary_table_columns_width', str, '')
    SIDEBAR_VISIBLE = _StoredSettingMeta('sidebar_visible', bool, True)


class Settings:
    @staticmethod
    def _qt_adapter():
        return QSettings(PUBLISHER_NAME, PROJECT_NAME)

    @classmethod
    def set(cls, key: StoredSettings, value):
        assert (isinstance(value, key.value.type))
        cls._qt_adapter().setValue(key.value.stored_name, value)

    @classmethod
    def get(cls, key: StoredSettings):
        return cls._qt_adapter().value(key.value.stored_name, defaultValue=key.value.default_value, type=key.value.type)
