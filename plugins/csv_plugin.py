from pathlib import Path
import pandas as pd

from plugins.base_plugin import BasePlugin
from core.models import Schema, ColumnInfo


class CSVPlugin(BasePlugin):

    name = "csv"

    def detect(self, file_path: Path) -> bool:
        return file_path.suffix.lower() == ".csv"

    # -------------------------
    # Preview
    # -------------------------

    def read_preview(self, file_path: Path, rows: int = 100):

        df = pd.read_csv(file_path, nrows=rows)

        return df

    # -------------------------
    # Full dataset
    # -------------------------

    def read_full(self, file_path: Path):

        df = pd.read_csv(file_path)

        return df

    # -------------------------
    # Schema detection
    # -------------------------

    def detect_schema(self, data):

        columns = []

        for col in data.columns:

            dtype = str(data[col].dtype)

            sample_values = (
                data[col]
                .dropna()
                .astype(str)
                .head(5)
                .tolist()
            )

            column = ColumnInfo(
                name=col,
                dtype=dtype,
                nullable=data[col].isnull().any(),
                sample_values=sample_values
            )

            columns.append(column)

        return Schema(columns=columns)