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
