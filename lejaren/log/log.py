from pathlib import Path

import logging
import logging.config
import os

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = PROJECT_ROOT / "log" / "lejaren.log"

def get_logger() -> logging.Logger:
    """Return a logging.Logger object w/ default of info.
    can specify level with LEJAREN_LOG_LEVEL.
    """

    log_level = os.getenv("LEJAREN_LOG_LEVEL", "INFO").upper()

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False, #to play nice...
            "formatters": {
                "f": {
                    "format": "[%(levelname)s] %(asctime)s (%(process)d) %(module)s: %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "s": {
                    "class": "logging.StreamHandler",
                    "formatter": "f",
                    "level": log_level,
                },
                "f": {
                    "class": "logging.FileHandler",
                    "mode": "w",
                    "formatter": "f",
                    "level": log_level,
                    "filename": LOG_FILE,
                }
            },
            "loggers": {"default": {"handlers": ["s", "f"], "level": log_level}},
        }
    )

    return logging.getLogger("default")