"""
SQLite Loader
-------------

Loader encargado de insertar datos en una base SQLite.

Implementa operaciones básicas:
- conexión
- creación opcional de tabla
- inserción de registros
"""

import sqlite3
from pathlib import Path
from typing import Iterable, Dict, Any, List

from core.exceptions import LoaderError


class SQLiteLoader:
    """
    Loader para SQLite.

    connection_string ejemplo:
        sqlite:///ruta/a/archivo.db
    """

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None

    # ---------------------------------------------------------
    # conexión
    # ---------------------------------------------------------

    def connect(self):
        """
        Abre conexión SQLite.
        """

        try:
            db_path = self._parse_connection_string(self.connection_string)

            Path(db_path).parent.mkdir(parents=True, exist_ok=True)

            self.connection = sqlite3.connect(db_path)

        except Exception as e:
            raise LoaderError(f"Error conectando a SQLite: {e}")

    # ---------------------------------------------------------

    def close(self):
        if self.connection:
            self.connection.close()

    # ---------------------------------------------------------
    # insertar registros
    # ---------------------------------------------------------

    def insert_rows(
        self,
        table_name: str,
        rows: Iterable[Dict[str, Any]],
        create_if_missing: bool = True
    ):
        """
        Inserta filas en la tabla.

        rows debe ser iterable de dicts
        """

        rows = list(rows)

        if not rows:
            return

        cursor = self.connection.cursor()

        columns = list(rows[0].keys())

        if create_if_missing:
            self._ensure_table(cursor, table_name, columns)

        placeholders = ", ".join(["?"] * len(columns))
        column_sql = ", ".join(columns)

        query = f"""
        INSERT INTO {table_name} ({column_sql})
        VALUES ({placeholders})
        """

        values = [
            tuple(row.get(col) for col in columns)
            for row in rows
        ]

        try:
            cursor.executemany(query, values)
            self.connection.commit()

        except Exception as e:
            raise LoaderError(f"Error insertando filas: {e}")

    # ---------------------------------------------------------
    # crear tabla automática
    # ---------------------------------------------------------

    def _ensure_table(self, cursor, table_name: str, columns: List[str]):
        """
        Crea tabla si no existe.

        Por ahora todos los campos TEXT.
        """

        cols_sql = ", ".join(f"{c} TEXT" for c in columns)

        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {cols_sql}
        )
        """

        cursor.execute(query)

    # ---------------------------------------------------------
    # utils
    # ---------------------------------------------------------

    def _parse_connection_string(self, conn: str) -> str:
        """
        Convierte:

        sqlite:///data/test.db
        """

        if not conn.startswith("sqlite:///"):
            raise LoaderError("Connection string SQLite inválido")

        return conn.replace("sqlite:///", "")
