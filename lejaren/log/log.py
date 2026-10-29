import logging
import logging.config
import os

def get_logger() -> logging.Logger:
    """Return a logging.Logger object w/ default of info.
    can specify level with P2XML_LOG_LEVEL.
    """

    log_level = os.getenv("P2XML_LOG_LEVEL", "INFO").upper()

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "f": {
                    "format": "[%(levelname)s] %(asctime)s (%(process)d) %(module)s: %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "h": {
                    "class": "logging.StreamHandler",
                    "formatter": "f",
                    "level": log_level,

                }
            },
            "loggers": {"default": {"handlers": ["h"], "level": log_level}},
        }
    )

    return logging.getLogger("default")