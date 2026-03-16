from plugins.excel_plugin import ExcelPlugin
from plugins.base_plugin import BasePlugin
from plugins.base_plugin import PluginError
# gui/plugins/excel_plugin.py
import pandas as pd
from .base_plugin import BasePlugin, PluginError

class ExcelPlugin(BasePlugin):

    def read_rows(self):
        try:
            df = pd.read_excel(self.file_path)
            if df.empty:
                raise PluginError("Archivo Excel vacío")
            for _, row in df.iterrows():
                yield row.to_dict()
        except FileNotFoundError:
            raise PluginError(f"Archivo no encontrado: {self.file_path}")
        except Exception as e:
            raise PluginError(f"Error leyendo Excel: {str(e)}")

    @staticmethod
    def detect(file_path: str) -> bool:
        return file_path.lower().endswith(('.xls', '.xlsx'))
