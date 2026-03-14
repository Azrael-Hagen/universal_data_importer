from core.models import ImportResult
from core.models import ImportConfig
from core.models import DatabaseConfig
from core.models import ColumnMapping
from core.models import PreviewData
from core.models import Schema
from core.models import ColumnInfo
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# --------------------------------------------------
# Column information
# --------------------------------------------------

@dataclass
class ColumnInfo:
    """
    Describes a column detected in the dataset.
    """

    name: str
    dtype: str
    nullable: bool = True
    sample_values: List[Any] = field(default_factory=list)


# --------------------------------------------------
# Dataset schema
# --------------------------------------------------

@dataclass
class Schema:
    """
    Represents the structure of a dataset.
    """

    columns: List[ColumnInfo]

    def column_names(self) -> List[str]:
        return [c.name for c in self.columns]

    def get_column(self, name: str) -> Optional[ColumnInfo]:

        for col in self.columns:
            if col.name == name:
                return col

        return None


# --------------------------------------------------
# Preview data
# --------------------------------------------------

@dataclass
class PreviewData:
    """
    Holds preview data from a dataset.
    """

    rows: List[Dict[str, Any]]
    schema: Optional[Schema] = None


# --------------------------------------------------
# Column mapping
# --------------------------------------------------

@dataclass
class ColumnMapping:
    """
    Mapping between source and destination column.
    """

    source_column: str
    target_column: str


# --------------------------------------------------
# Database configuration
# --------------------------------------------------

@dataclass
class DatabaseConfig:
    """
    Database connection configuration.
    """

    db_type: str

    host: Optional[str] = None
    port: Optional[int] = None

    database: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None

    file_path: Optional[str] = None  # For SQLite


# --------------------------------------------------
# Import configuration
# --------------------------------------------------

@dataclass
class ImportConfig:
    """
    Full configuration for an import job.
    """

    table_name: str
    mappings: List[ColumnMapping]
    create_table: bool = True
    batch_size: int = 1000


# --------------------------------------------------
# Import result
# --------------------------------------------------

@dataclass
class ImportResult:
    """
    Result of an import operation.
    """

    success: bool
    rows_imported: int = 0
    errors: List[str] = field(default_factory=list)