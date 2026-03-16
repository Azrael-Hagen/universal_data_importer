from core.models import Schema
from core.exceptions import ImportExecutionError
from core.exceptions import DatabaseConnectionError
from core.exceptions import SchemaDetectionError
from core.exceptions import UnsupportedFormatError
from core.exceptions import ImporterError
class ImporterError(Exception):
    """Base exception for the importer."""


class UnsupportedFormatError(ImporterError):
    pass


class SchemaDetectionError(ImporterError):
    pass


class DatabaseConnectionError(ImporterError):
    pass


class ImportExecutionError(ImporterError):
    pass
