from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ColumnInfo:
    name: str
    dtype: str
    nullable: bool = True
    sample_values: List[Any] = field(default_factory=list)


@dataclass
class Schema:
    columns: List[ColumnInfo]


@dataclass
class Mapping:
    source_column: str
    target_column: str


@dataclass
class ImportConfig:
    table_name: str
    mappings: List[Mapping]
    create_table: bool = True
