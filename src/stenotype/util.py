from logging import getLogger
from logging.config import dictConfig

log = getLogger(__name__)


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
