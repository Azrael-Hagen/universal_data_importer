import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import List, Optional


# =========================================================
# ESTRUCTURAS
# =========================================================

@dataclass
class ColumnSchema:

    name: str
    pandas_type: str
    sql_type: str
    nullable: bool
    unique: bool
    null_ratio: float
    is_enum: bool = False
    enum_values: Optional[List[str]] = None
    indexed: bool = False


@dataclass
class SchemaResult:

    table_name: str
    columns: List[ColumnSchema]
    primary_key: Optional[str]


# =========================================================
# DETECTOR
# =========================================================

class SchemaDetector:

    ENUM_THRESHOLD = 20
    INDEX_UNIQUE_RATIO = 0.8

    def detect(self, df: pd.DataFrame, table_name: str = "imported_table") -> SchemaResult:

        columns = []

        for col in df.columns:

            series = df[col]

            pandas_type = str(series.dtype)

            nullable = series.isnull().any()

            null_ratio = series.isnull().sum() / len(series)

            unique = series.is_unique

            sql_type = self._detect_sql_type(series)

            is_enum, enum_values = self._detect_enum(series)

            indexed = self._should_index(series)

            column_schema = ColumnSchema(
                name=col,
                pandas_type=pandas_type,
                sql_type=sql_type,
                nullable=nullable,
                unique=unique,
                null_ratio=null_ratio,
                is_enum=is_enum,
                enum_values=enum_values,
                indexed=indexed
            )

            columns.append(column_schema)

        primary_key = self._detect_primary_key(df)

        return SchemaResult(
            table_name=table_name,
            columns=columns,
            primary_key=primary_key
        )


# =========================================================
# DETECTOR DE TIPOS
# =========================================================

    def _detect_sql_type(self, series: pd.Series) -> str:

        dtype = series.dtype

        if pd.api.types.is_integer_dtype(dtype):
            return "INTEGER"

        if pd.api.types.is_float_dtype(dtype):
            return "FLOAT"

        if pd.api.types.is_bool_dtype(dtype):
            return "BOOLEAN"

        if pd.api.types.is_datetime64_any_dtype(dtype):
            return "DATETIME"

        # intentar detectar booleano en texto
        if self._looks_like_boolean(series):
            return "BOOLEAN"

        # intentar detectar fechas en texto
        if self._looks_like_datetime(series):
            return "DATETIME"

        # string
        max_len = series.astype(str).str.len().max()

        if max_len and max_len < 255:
            return f"VARCHAR({max_len})"

        return "TEXT"


# =========================================================
# DETECCIÓN BOOLEAN
# =========================================================

    def _looks_like_boolean(self, series: pd.Series) -> bool:

        values = series.dropna().astype(str).str.lower().unique()

        boolean_values = {
            "true", "false",
            "yes", "no",
            "1", "0",
            "t", "f"
        }

        return set(values).issubset(boolean_values)


# =========================================================
# DETECCIÓN FECHAS
# =========================================================

    def _looks_like_datetime(self, series: pd.Series) -> bool:

        sample = series.dropna().astype(str).head(50)

        success = 0

        for value in sample:

            try:
                pd.to_datetime(value)
                success += 1
            except:
                pass

        if len(sample) == 0:
            return False

        ratio = success / len(sample)

        return ratio > 0.8


# =========================================================
# DETECCIÓN ENUM
# =========================================================

    def _detect_enum(self, series: pd.Series):

        unique_values = series.dropna().unique()

        if len(unique_values) <= self.ENUM_THRESHOLD:

            return True, list(map(str, unique_values))

        return False, None


# =========================================================
# DETECCIÓN ÍNDICE
# =========================================================

    def _should_index(self, series: pd.Series):

        unique_ratio = series.nunique() / len(series)

        if unique_ratio > self.INDEX_UNIQUE_RATIO:

            return True

        return False


# =========================================================
# DETECCIÓN PRIMARY KEY
# =========================================================

    def _detect_primary_key(self, df: pd.DataFrame) -> Optional[str]:

        # prioridad columnas llamadas id

        for col in df.columns:

            if col.lower() == "id":

                series = df[col]

                if series.is_unique and not series.isnull().any():
                    return col

        # buscar columna única

        for col in df.columns:

            series = df[col]

            if series.is_unique and not series.isnull().any():

                return col

        return None