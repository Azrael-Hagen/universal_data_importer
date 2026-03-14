"""
CSV Plugin
----------

Plugin para leer archivos CSV.

Características:

- lectura streaming
- batch processing
- encoding configurable
- delimitador configurable
"""

import csv
from typing import Iterator, Dict, Any, List

from plugins.base_plugin import BasePlugin
from plugins.plugin_registry import PluginRegistry
from core.exceptions import PluginError


class CSVPlugin(BasePlugin):

    name = "csv"

    def __init__(self, file_path: str, delimiter: str = ",", encoding: str = "utf-8"):
        self.file_path = file_path
        self.delimiter = delimiter
        self.encoding = encoding

    # ---------------------------------------------------------

    def read_rows(self) -> Iterator[Dict[str, Any]]:
        """
        Lee el CSV fila por fila.
        """

        try:

            with open(self.file_path, "r", encoding=self.encoding, newline="") as f:

                reader = csv.DictReader(f, delimiter=self.delimiter)

                for row in reader:
                    yield row

        except Exception as e:
            raise PluginError(f"Error leyendo CSV: {e}")

    # ---------------------------------------------------------

    def read_batches(self, batch_size: int) -> Iterator[List[Dict[str, Any]]]:
        """
        Devuelve batches de filas.
        """

        batch = []

        for row in self.read_rows():

            batch.append(row)

            if len(batch) >= batch_size:

                yield batch
                batch = []

        if batch:
            yield batch


# registrar plugin
PluginRegistry.register("csv", CSVPlugin)
