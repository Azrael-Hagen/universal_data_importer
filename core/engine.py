"""
ImportEngine

Core ETL engine used by Universal Data Importer.
"""

import pandas as pd

from loaders.sqlite_loader import SQLiteLoader
from config.settings import PREVIEW_ROWS, BATCH_SIZE, SQLITE_DB_PATH, DEFAULT_TABLE_NAME


class ImportEngine:

    def __init__(
        self,
        state,
        progress_callback=None,
        log_callback=None,
    ):

        self.state = state

        self.progress = progress_callback
        self.log = log_callback

        self.file_path = state["file_path"]
        self.file_format = state["format"]

        self.schema = state["schema"]
        self.mapping = state["mapping"]

        self.loader = None

    # --------------------------------------------------

    def run(self):

        """
        Execute the full import process.
        """

        self._log("Starting import engine")

        # Create loader
        self.loader = SQLiteLoader(
            db_path=SQLITE_DB_PATH,
            table_name=DEFAULT_TABLE_NAME,
            schema=self.schema,
            log_callback=self.log
        )

        self.loader.connect()
        self.loader.create_table()

        df = self.load_source()

        df = self.apply_mapping(df)

        df = self.apply_transforms(df)

        rows, errors = self.batch_insert(df)

        self.loader.close()

        self._log("Import completed")

        return rows, errors

    # --------------------------------------------------

    def load_source(self):

        self._log(f"Loading source file: {self.file_path}")

        if self.file_format == "csv":
            df = pd.read_csv(self.file_path)

        elif self.file_format == "excel":
            df = pd.read_excel(self.file_path)

        elif self.file_format == "json":
            df = pd.read_json(self.file_path)

        elif self.file_format == "xml":
            df = pd.read_xml(self.file_path)

        else:
            raise ValueError(f"Unsupported format: {self.file_format}")

        self._log(f"Loaded {len(df)} rows")

        return df

    # --------------------------------------------------

    def apply_mapping(self, df):

        self._log("Applying column mapping")

        rename_map = {}

        for m in self.mapping:

            source = m["source"]
            target = m["target"]

            if target:
                rename_map[source] = target

        df = df.rename(columns=rename_map)

        return df

    # --------------------------------------------------

    def apply_transforms(self, df):

        self._log("Applying transformations")

        for m in self.mapping:

            col = m["target"]
            transform = m["transform"]

            if not col or col not in df.columns:
                continue

            if transform == "TRIM":
                df[col] = df[col].astype(str).str.strip()

            elif transform == "LOWER":
                df[col] = df[col].astype(str).str.lower()

            elif transform == "UPPER":
                df[col] = df[col].astype(str).str.upper()

            elif transform == "INT":
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

            elif transform == "FLOAT":
                df[col] = pd.to_numeric(df[col], errors="coerce")

            elif transform == "BOOLEAN":
                df[col] = df[col].astype(bool)

        return df

    # --------------------------------------------------

    def batch_insert(self, df, batch_size=BATCH_SIZE):

        self._log("Starting batch insert")

        total = len(df)

        processed = 0
        errors = 0

        for start in range(0, total, batch_size):

            batch = df.iloc[start : start + batch_size]

            try:

                self.insert_batch(batch)

                processed += len(batch)

            except Exception as e:

                errors += len(batch)

                self._log(f"Batch error: {str(e)}")

            percent = int((processed / total) * 100)

            if self.progress:
                self.progress(percent)

        return processed, errors

    # --------------------------------------------------

    def insert_batch(self, batch_df):

        rows = batch_df.to_dict(orient="records")

        self.loader.insert_batch(rows)

    # --------------------------------------------------

    def _log(self, message):

        if self.log:
            self.log(message)