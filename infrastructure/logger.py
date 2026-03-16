import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from infrastructure.config_manager import ConfigManager


_initialized = False


def setup_logging(config: ConfigManager):
    """
    Initialize logging configuration.
    """

    global _initialized

    if _initialized:
        return

    log_level = config.get("logging.level", "INFO").upper()

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "udi.log"

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # -----------------------------
    # Console handler
    # -----------------------------

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)

    # -----------------------------
    # File handler with rotation
    # -----------------------------

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5_000_000,
        backupCount=3
    )

    file_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)

    _initialized = True


def get_logger(name: str):

    return logging.getLogger(name)