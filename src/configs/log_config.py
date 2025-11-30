from functools import lru_cache
from typing import Literal
from enum import StrEnum
import logging
from logging import Logger, Formatter
from logging.handlers import RotatingFileHandler
import os

class LoggingLevels(StrEnum):
    INFO = "info"
    DEBUG = "debug"


@lru_cache(maxsize=1)
def setup_logger(logger_name: str, level: Literal["info", "debug"] = "info") -> Logger:
    """
    Setup the program's logger.

    ### Args:
    - logger_name (str): The name of the logger (The file in which the logger was created)
    - level ("info" | "debug"): logging level in which the system will

    ### Returns:
        The logger instance
    """
    # Lazy import to avoid circular dependency
    from src import settings

    os.makedirs(settings.LOGS_DIR, exist_ok=True)

    logger = logging.getLogger(logger_name)

    if level == LoggingLevels.INFO:
        logger.setLevel(logging.INFO)
    elif level == LoggingLevels.DEBUG:
        logger.setLevel(logging.DEBUG)

    format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

    formatter = Formatter(
        fmt=format,
        datefmt="%Y-%m-%d %H:%M:%S:%z"    
    )

    file_handler = RotatingFileHandler(
        filename=f"{settings.LOGS_DIR}/{level}_logs.log",
        maxBytes=3_000_000,
        backupCount=5,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger
