from plugins.csv_plugin import CSVPlugin
from plugins.base_plugin import BasePlugin
from plugins.base_plugin import PluginError
# gui/plugins/csv_plugin.py
import csv
from .base_plugin import BasePlugin, PluginError

class CSVPlugin(BasePlugin):

    def read_rows(self):
        try:
            with open(self.file_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    raise PluginError("CSV sin encabezados o vacío")
                for row in reader:
                    yield dict(row)
        except FileNotFoundError:
            raise PluginError(f"Archivo no encontrado: {self.file_path}")
        except UnicodeDecodeError:
            raise PluginError(f"Error de codificación en: {self.file_path}")
        except Exception as e:
            raise PluginError(f"Error leyendo CSV: {str(e)}")

    @staticmethod
    def detect(file_path: str) -> bool:
        return file_path.lower().endswith('.csv')
