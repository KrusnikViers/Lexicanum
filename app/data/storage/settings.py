from collections import namedtuple
from enum import Enum

from PySide2.QtCore import QSettings

from app.info import PROJECT_NAME, PUBLISHER_NAME

_StoredSettingMeta = namedtuple('StoredSettingMeta', 'type default_value')


# Add new values to be stored in this enum.
class StoredSettings(Enum):
    LAST_IMPORT_PATH = _StoredSettingMeta(str, '')
    LAST_EXPORT_PATH = _StoredSettingMeta(str, '')
    IMPORT_ON_STARTUP = _StoredSettingMeta(bool, True)


class Settings:
    @staticmethod
    def _qt_adapter():
        return QSettings(PUBLISHER_NAME, PROJECT_NAME)

    @staticmethod
    def set(key: StoredSettings, value):
        Settings._qt_adapter().setValue(key.name, value)

    @staticmethod
    def get(key: StoredSettings):
        return Settings._qt_adapter().value(key.name, defaultValue=key.value.default_value, type=key.value.type)
