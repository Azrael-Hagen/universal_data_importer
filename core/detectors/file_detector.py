from pathlib import Path

def detect_file_type(path):

    ext = Path(path).suffix.lower()

    if ext == ".csv":
        return "csv"

    if ext in [".xlsx", ".xls"]:
        return "excel"

    if ext == ".json":
        return "json"

    return "unknown"