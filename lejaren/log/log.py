from pathlib import Path

import logging
import logging.config
import os

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = PROJECT_ROOT / "log" / "lejaren.log"

log_types = ('default', 'stream_only', 'file_only')

def get_logger(log_type="default") -> logging.Logger:
    """Return a logging.Logger object w/ default of info.
    can specify level with LEJAREN_LOG_LEVEL.
    """

    if log_type not in log_types:
        print("Default Log...")
        log_type = 'default'
    else:
        # log_type is ok..
        pass

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
            "loggers": {
                "default": {"handlers": ["s", "f"], "level": log_level},
                "stream_only": {"handlers": ["s"], "level": log_level},
                "file_only": {"handlers": ["f"], "level": log_level}
            }
        }
    )

    return logging.getLogger(log_type)