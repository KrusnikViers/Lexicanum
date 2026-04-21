"""Network API wrapper for AnkiConnect. Manages connection status and calls execution."""
import enum
import logging
from dataclasses import dataclass
from datetime import timedelta

import requests
from PySide6.QtCore import QObject, Slot, Signal, QTimer

from base import settings

_ANKI_CONNECT_API_VERSION = 5
_CONNECTION_TIMEOUT = timedelta(milliseconds=250)
_CONNECTION_CHECK_INTERVAL = timedelta(seconds=0.5)
_CONNECTION_CHECK_MAX_INTERVAL = timedelta(seconds=3)


def _timedelta_to_msec(interval: timedelta) -> int:
    result = int(interval.total_seconds() * 1000)
    if interval.total_seconds() > 0 and result == 0:
        raise ValueError("Timedelta cannot be correctly represented in msec.")
    return result


class ConnectionStatus(enum.IntEnum):
    NOT_SET = 0
    CONNECTED = 1
    DISCONNECTED = 2


@dataclass
class ConnectionCheckResult:
    status: ConnectionStatus
    error: str | None = None


def _get_url_from_settings():
    url = f'{settings.ANKI_CONNECT_URL.get()}:{settings.ANKI_CONNECT_PORT.get()}'
    if url.startswith('http'):
        return url
    return 'http://' + url


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

        self.check_connection()

    @property
    def status(self) -> ConnectionStatus:
        return self._status

    def get(self, params: dict) -> dict | None:
        """Internal implementation of GET, returns response body or detailed DISCONNECT description."""
        params.update({'version': _ANKI_CONNECT_API_VERSION})
        try:
            response = self._session.get(url=self._url, json=params, timeout=_CONNECTION_TIMEOUT.total_seconds())
            self._update_connection_state(ConnectionCheckResult(ConnectionStatus.CONNECTED))
            return response.json()

        except requests.exceptions.RequestException as request_exc:
            error_type = type(request_exc).__name__
            reason = str(request_exc.args[0]) if request_exc.args else str(request_exc)
            check_result = ConnectionCheckResult(ConnectionStatus.DISCONNECTED, f"{error_type}: {reason}")
            self._update_connection_state(check_result)
            return None

    def _update_connection_state(self, check_result: ConnectionCheckResult) -> None:
        if check_result.status == self._status:
            # Double the check interval and return early.
            max_interval = _timedelta_to_msec(_CONNECTION_CHECK_MAX_INTERVAL)
            current_interval = self._status_check_timer.interval()
            if current_interval < max_interval:
                self._status_check_timer.setInterval(min(max_interval, current_interval * 2))
            return

        self._status = check_result.status
        logging.info(f"Connection status changed to {check_result.status.name} : {check_result.error}")
        self.status_change.emit(self._status)

    @Slot()
    def maybe_refresh_connection(self) -> None:
        new_url = _get_url_from_settings()
        if self._status == ConnectionStatus.CONNECTED and new_url == self._url:
            return

        self._session.close()
        self._session = requests.Session()
        self._url = new_url
        self.check_connection()

    @Slot()
    def check_connection(self) -> None:
        self.get({'action': 'version'})
