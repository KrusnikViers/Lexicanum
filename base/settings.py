# Usage: Settings object is safe to be cached, and cheap to recreate if needed.
# Add new values to the `Settings` enum for both settings that are visible to the user, or simply caching some values
# between sessions.

from dataclasses import dataclass
from typing import TypeVar, Type, Generic, Any

from PySide6.QtCore import QSettings, QRect

from base import info

_SType = TypeVar("_SType")


def _qt_adapter() -> QSettings:
    # QSettings implementation takes care of the values caching. Creating/destructing this wrapper is very fast.
    return QSettings(info.PUBLISHER_NAME, info.PROJECT_NAME)


@dataclass
class OptionDefinition(Generic[_SType]):
    name: str
    type: Type[_SType]
    default: _SType

    def set(self, value: Any) -> None:
        if not isinstance(value, self.type):
            raise TypeError(f"Wrong type to set for {self.name}: {type(value)} vs {self.type}")
        _qt_adapter().setValue(self.name, value)

    def get(self) -> _SType:
        return _qt_adapter().value(self.name, defaultValue=self.default, type=self.type)


# Add new settings (values to be stored persistently between launches) below.
# Separate groups of settings as group_name/setting_name: MY_VALUE = OptionDefinition('base/my_setting', int, 42).
# To use in code, call MY_VALUE.set(43) and MY_VALUE.get().
UI_MAIN_WINDOW_GEOMETRY = OptionDefinition('ui/main_window_geometry', QRect, QRect())
