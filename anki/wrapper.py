"""Primary interface for the Anki connection."""
from PySide6.QtCore import QObject

from anki import connection as anki_connection

_ANKI_CONNECT_VERSION = 5


class AnkiWrapper(QObject):
    def __init__(self, *,
                 connection: anki_connection.Connection | None = None):
        super().__init__()
        self.connection = connection if connection is not None else anki_connection.Connection()
