from plugins.xml_plugin import XMLPlugin
from plugins.base_plugin import BasePlugin
from plugins.base_plugin import PluginError
# gui/plugins/xml_plugin.py
import xml.etree.ElementTree as ET
from .base_plugin import BasePlugin, PluginError

class XMLPlugin(BasePlugin):

    def read_rows(self):
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            if not list(root):
                raise PluginError("XML vacío o sin nodos")
            for child in root:
                row = {elem.tag: elem.text for elem in child}
                yield row
        except FileNotFoundError:
            raise PluginError(f"Archivo no encontrado: {self.file_path}")
        except ET.ParseError:
            raise PluginError(f"XML inválido o corrupto: {self.file_path}")
        except Exception as e:
            raise PluginError(f"Error leyendo XML: {str(e)}")

    @staticmethod
    def detect(file_path: str) -> bool:
        return file_path.lower().endswith('.xml')
