# gui/plugins/json_plugin.py
import pandas as pd
from .base_plugin import BasePlugin, PluginError

class JSONPlugin(BasePlugin):

    def read_rows(self):
        try:
            df = pd.read_json(self.file_path)
            if df.empty:
                raise PluginError("Archivo JSON vacío")
            for _, row in df.iterrows():
                yield row.to_dict()
        except FileNotFoundError:
            raise PluginError(f"Archivo no encontrado: {self.file_path}")
        except ValueError:
            raise PluginError(f"JSON inválido o corrupto: {self.file_path}")
        except Exception as e:
            raise PluginError(f"Error leyendo JSON: {str(e)}")

    @staticmethod
    def detect(file_path: str) -> bool:
        return file_path.lower().endswith('.json')
