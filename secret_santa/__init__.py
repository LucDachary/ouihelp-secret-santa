import logging
import logging.config

LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "detailed": {
            "class": "logging.Formatter",
            "format": "%(asctime)s [%(name)-15.15s] %(levelname)-5.5s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            # Change this to "DEBUG" to see traces in console.
            "level": "INFO",
            "formatter": "detailed",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"]
    },
}

logging.config.dictConfig(LOG_CONFIG)
