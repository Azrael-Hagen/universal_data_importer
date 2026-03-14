"""
Application Settings

Central configuration file for Universal Data Importer.
All modules should import configuration values from here
instead of hardcoding parameters.
"""

from pathlib import Path
from config.settings import PREVIEW_ROWS, BATCH_SIZE, SQLITE_DB_PATH, DEFAULT_TABLE_NAME


# --------------------------------------------------
# Project Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# File Import Settings
# --------------------------------------------------

# Number of rows used for preview
PREVIEW_ROWS = 200

# Maximum allowed file size (MB)
MAX_FILE_SIZE_MB = 5000


# --------------------------------------------------
# Engine Settings
# --------------------------------------------------

# Batch insert size
BATCH_SIZE = 500

# Chunk size for very large files (future use)
CHUNK_SIZE = 10000


# --------------------------------------------------
# Supported Formats
# --------------------------------------------------

SUPPORTED_FORMATS = [
    "csv",
    "excel",
    "json",
    "xml",
]


# --------------------------------------------------
# Database Settings
# --------------------------------------------------

DEFAULT_DB_TYPE = "sqlite"

SQLITE_DB_PATH = BASE_DIR / SQLITE_DB_PATH

DEFAULT_TABLE_NAME = DEFAULT_TABLE_NAME


# --------------------------------------------------
# Logging Settings
# --------------------------------------------------

LOG_LEVEL = "INFO"

LOG_FILE = LOG_DIR / "importer.log"


# --------------------------------------------------
# GUI Settings
# --------------------------------------------------

APP_NAME = "Universal Data Importer"

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600