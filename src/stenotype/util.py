"""Utility functions and constants for stenotype.

Functions and constants that are general purpose and do not belong to any module in
particular should be collected here.

When adding code to this file, please take note that it should always be importable from
any point in the project in order to retain its global status. As a consequence, it can't
import anything from the project itself (e.g. "import stenotypes.something"), since that
would lead to circular dependencies down the line. Code that is needed here should always
have been here from the start.
"""
from logging import getLogger
from logging.config import dictConfig

log = getLogger(__name__)


class StenotypeException(Exception):
    pass


def setup_logging(loglevel: str):
    """Set up basic logging to stdout.

    Args:
        loglevel: Can be any of [DEBUG, INFO, WARNING, ERROR, CRITICAL]

    """
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
                }
            },
            "handlers": {
                "default": {
                    "level": loglevel,
                    "formatter": "standard",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                }
            },
            "loggers": {
                "": {"handlers": ["default"], "level": loglevel, "propagate": True}
            },
        }
    )
