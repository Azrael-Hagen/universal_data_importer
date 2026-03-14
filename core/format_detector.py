import os
import csv
import zipfile
import gzip
from dataclasses import dataclass
from typing import Optional

import chardet


# =========================================================
# RESULTADO DE DETECCIÓN
# =========================================================

@dataclass
class DetectionResult:

    format: str
    encoding: Optional[str] = None
    delimiter: Optional[str] = None
    compression: Optional[str] = None
    confidence: float = 0.0


# =========================================================
# CONFIGURACIÓN
# =========================================================

TEXT_SAMPLE_SIZE = 4096
BINARY_SAMPLE_SIZE = 32


EXTENSION_MAP = {

    ".csv": "csv",
    ".tsv": "csv",
    ".txt": "csv",

    ".json": "json",
    ".jsonl": "json",

    ".xml": "xml",

    ".xlsx": "excel",
    ".xls": "excel",
    ".xlsb": "excel",

    ".parquet": "parquet",

    ".dbf": "dbf",

    ".sqlite": "sqlite",
    ".db": "sqlite",

    ".zip": "zip",
    ".gz": "gzip"
}


# =========================================================
# DETECTOR PRINCIPAL
# =========================================================

class FormatDetector:

    def detect(self, file_path: str) -> DetectionResult:

        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)

        # 1 extensión
        fmt = self._detect_by_extension(file_path)

        # 2 magic bytes
        magic_fmt = self._detect_magic(file_path)

        if magic_fmt:
            fmt = magic_fmt

        # 3 compresión
        compression = self._detect_compression(file_path)

        # 4 encoding
        encoding = self._detect_encoding(file_path)

        # 5 delimitador
        delimiter = None
        if fmt == "csv":
            delimiter = self._detect_delimiter(file_path, encoding)

        # 6 análisis de contenido si aún no sabemos
        if fmt is None:
            fmt = self._detect_by_content(file_path, encoding)

        return DetectionResult(
            format=fmt or "unknown",
            encoding=encoding,
            delimiter=delimiter,
            compression=compression,
            confidence=0.9 if fmt else 0.3
        )



# =========================================================
# DETECCIÓN POR EXTENSIÓN
# =========================================================

    def _detect_by_extension(self, file_path):

        ext = os.path.splitext(file_path)[1].lower()

        return EXTENSION_MAP.get(ext)



# =========================================================
# DETECCIÓN POR MAGIC BYTES
# =========================================================

    def _detect_magic(self, file_path):

        try:

            with open(file_path, "rb") as f:
                header = f.read(BINARY_SAMPLE_SIZE)

            if header.startswith(b"PK"):
                return "excel"

            if header.startswith(b"PAR1"):
                return "parquet"

            if b"SQLite format 3" in header:
                return "sqlite"

            if header.startswith(b"\x1f\x8b"):
                return "gzip"

        except Exception:
            pass

        return None



# =========================================================
# DETECCIÓN DE COMPRESIÓN
# =========================================================

    def _detect_compression(self, file_path):

        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".zip":
            return "zip"

        if ext == ".gz":
            return "gzip"

        return None



# =========================================================
# DETECCIÓN DE ENCODING
# =========================================================

    def _detect_encoding(self, file_path):

        try:

            with open(file_path, "rb") as f:
                raw = f.read(TEXT_SAMPLE_SIZE)

            result = chardet.detect(raw)

            return result["encoding"]

        except Exception:
            return None



# =========================================================
# DETECCIÓN DE DELIMITADOR
# =========================================================

    def _detect_delimiter(self, file_path, encoding):

        try:

            with open(file_path, "r", encoding=encoding or "utf-8") as f:
                sample = f.read(TEXT_SAMPLE_SIZE)

            dialect = csv.Sniffer().sniff(sample)

            return dialect.delimiter

        except Exception:
            return None



# =========================================================
# DETECCIÓN POR CONTENIDO
# =========================================================

    def _detect_by_content(self, file_path, encoding):

        try:

            with open(file_path, "r", encoding=encoding or "utf-8") as f:
                sample = f.read(TEXT_SAMPLE_SIZE)

            s = sample.strip()

            if s.startswith("{") or s.startswith("["):
                return "json"

            if s.startswith("<"):
                return "xml"

            if "," in sample:
                return "csv"

        except Exception:
            pass

        return None