import logging
import sys
from types import MappingProxyType

LOGGING_LEVELS = MappingProxyType({
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'none': logging.CRITICAL + 1
})


def update_logging_configuration(level: str) -> None:
    logging.basicConfig(level=LOGGING_LEVELS[level],
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[logging.StreamHandler(sys.stdout),
                                  logging.FileHandler(filename="log.txt", encoding="utf-8")])
