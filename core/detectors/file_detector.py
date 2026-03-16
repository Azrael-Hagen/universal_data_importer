from pathlib import Path
import json
import sqlite3


# -----------------------------------------
# Public API
# -----------------------------------------

def detect_file_type(path: str) -> str:
    """
    Detect file type using multiple strategies.
    """

    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(path)

    # 1️⃣ Extension check
    ext = detect_by_extension(file_path)

    if ext:
        return ext

    # 2️⃣ Content detection
    for detector in DETECTORS:
        result = detector(file_path)
        if result:
            return result

    return "unknown"


# -----------------------------------------
# Extension detection
# -----------------------------------------

EXTENSION_MAP = {
    ".csv": "csv",
    ".xlsx": "excel",
    ".xls": "excel",
    ".json": "json",
    ".xml": "xml",
    ".sqlite": "sqlite",
    ".db": "sqlite",
    ".yaml": "yaml",
    ".yml": "yaml",
}


def detect_by_extension(path: Path):

    ext = path.suffix.lower()

    return EXTENSION_MAP.get(ext)


# -----------------------------------------
# Content detectors
# -----------------------------------------

def detect_csv(path: Path):

    try:
        with open(path, "r", encoding="utf-8") as f:
            line = f.readline()

        if "," in line or ";" in line:
            return "csv"
    except:
        pass


def detect_json(path: Path):

    try:
        with open(path, "r", encoding="utf-8") as f:
            json.load(f)

        return "json"
    except:
        pass


def detect_xml(path: Path):

    try:
        with open(path, "r", encoding="utf-8") as f:
            start = f.read(100)

        if "<?xml" in start or "<" in start:
            return "xml"
    except:
        pass


def detect_sqlite(path: Path):

    try:
        conn = sqlite3.connect(path)
        conn.execute("SELECT name FROM sqlite_master LIMIT 1")
        conn.close()

        return "sqlite"
    except:
        pass


# -----------------------------------------
# Detector registry
# -----------------------------------------

DETECTORS = [
    detect_json,
    detect_csv,
    detect_xml,
    detect_sqlite,
]