"""Network API wrapper for AnkiConnect. Manages connection status and calls execution."""
import enum
import logging
from datetime import timedelta

import requests
from PySide6.QtCore import QObject, Slot, Signal, QTimer

from base import settings

_ANKI_CONNECT_API_VERSION = 5
_CONNECTION_TIMEOUT = timedelta(seconds=5)
_CONNECTION_CHECK_INTERVAL = timedelta(milliseconds=500)


class ConnectionStatus(enum.IntEnum):
    NOT_SET = 0
    CONNECTED = 1
    DISCONNECTED = 2


def _get_url_from_settings():
    return f'{settings.ANKI_CONNECT_URL.get()}:{settings.ANKI_CONNECT_PORT.get()}'


def _timedelta_to_msec(interval: timedelta) -> int:
    result = int(interval.total_seconds() * 1000)
    if interval.total_seconds() > 0 and result == 0:
        raise ValueError("Timedelta cannot be correctly represented in msec.")
    return result


class Connection(QObject):
    status_change = Signal(ConnectionStatus)

    def __init__(self):
        super().__init__()
        self._url = _get_url_from_settings()
        self._session = requests.Session()
        self._status: ConnectionStatus = ConnectionStatus.NOT_SET

        # Note: Qt will not fire multiple signals if long call is being executed, so there is no need to halt the timer
        # even if some long request takes multiple firing intervals to execute.
        self._status_check_timer = QTimer(interval=_timedelta_to_msec(_CONNECTION_CHECK_INTERVAL))
        self._status_check_timer.timeout.connect(self.check_connection)
        self._status_check_timer.start()

    @property
    def status(self):
        return self._status

    def get(self, params: dict) -> dict | None:
        """Default method for retrieving the data. Appends supported AC version automatically."""
        params.update({'version': _ANKI_CONNECT_API_VERSION})
        try:
            response = self._session.get(url=self._url, json=params, timeout=_CONNECTION_TIMEOUT.total_seconds())
            return response.json()
        except (requests.exceptions.Timeout,
                requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                requests.exceptions.RequestException,):
            self._set_status(ConnectionStatus.DISCONNECTED)
        return None

    def _set_status(self, status: ConnectionStatus) -> None:
        if self._status == status:
            return
        self._status = status
        logging.info(f"Connection status changed: {status.name}")
        self.status_change.emit(status)

    @Slot()
    def maybe_refresh_connection(self) -> None:
        new_url = _get_url_from_settings()
        if self._status == ConnectionStatus.CONNECTED and new_url == self._url:
            return

        self._set_status(ConnectionStatus.DISCONNECTED)
        self._session.close()

        self._session = requests.Session()
        self._url = new_url
        self.check_connection()

    @Slot()
    def check_connection(self) -> None:
        check_result = self.get({'action': 'version'})
        if check_result is not None and 'error' in check_result and check_result['error'] is None:
            self._set_status(ConnectionStatus.CONNECTED)
        else:
            self._set_status(ConnectionStatus.DISCONNECTED)
