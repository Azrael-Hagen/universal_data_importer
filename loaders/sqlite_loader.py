"""
SQLiteLoader

Database loader used by Universal Data Importer
to insert data into SQLite databases.
"""

import sqlite3


class SQLiteLoader:

    def __init__(self, db_path, table_name, schema, log_callback=None):

        self.db_path = db_path
        self.table_name = table_name
        self.schema = schema

        self.log = log_callback

        self.conn = None
        self.cursor = None

    # --------------------------------------------------

    def connect(self):

        self.conn = sqlite3.connect(self.db_path)

        self.cursor = self.conn.cursor()

        self._log(f"Connected to SQLite: {self.db_path}")

    # --------------------------------------------------

    def create_table(self):

        """
        Create table using detected schema.
        """

        columns = self.schema["columns"]

        column_defs = []

        for col in columns:

            name = col["target_name"]
            dtype = self.sqlite_type(col["type"])

            col_def = f'"{name}" {dtype}'

            if col.get("primary_key"):
                col_def += " PRIMARY KEY"

            if not col.get("nullable", True):
                col_def += " NOT NULL"

            column_defs.append(col_def)

        sql = f"""
        CREATE TABLE IF NOT EXISTS "{self.table_name}" (
            {", ".join(column_defs)}
        )
        """

        self.cursor.execute(sql)

        self.conn.commit()

        self._log(f"Table ready: {self.table_name}")

    # --------------------------------------------------

    def insert_batch(self, rows):

        """
        Insert batch of rows into table.
        """

        if not rows:
            return

        columns = rows[0].keys()

        placeholders = ",".join(["?"] * len(columns))

        sql = f"""
        INSERT INTO "{self.table_name}"
        ({",".join(columns)})
        VALUES ({placeholders})
        """

        values = []

        for row in rows:

            values.append(tuple(row[c] for c in columns))

        self.cursor.executemany(sql, values)

        self.conn.commit()

    # --------------------------------------------------

    def sqlite_type(self, dtype):

        """
        Convert generic types to SQLite types.
        """

        mapping = {
            "INTEGER": "INTEGER",
            "FLOAT": "REAL",
            "BOOLEAN": "INTEGER",
            "TEXT": "TEXT",
            "DATE": "TEXT",
            "DATETIME": "TEXT",
            "JSON": "TEXT",
            "BLOB": "BLOB",
        }

        return mapping.get(dtype, "TEXT")

    # --------------------------------------------------

    def close(self):

        if self.conn:

            self.conn.close()

            self._log("SQLite connection closed")

    # --------------------------------------------------

    def _log(self, msg):

        if self.log:
            self.log(msg)