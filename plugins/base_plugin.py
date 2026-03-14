# gui/plugins/base_plugin.py
from abc import ABC, abstractmethod

class PluginError(Exception):
    """Error específico de plugins de importación."""
    pass

class BasePlugin(ABC):
    """
    Clase base para todos los plugins de importación.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    @abstractmethod
    def read_rows(self):
        """
        Debe devolver un iterador de diccionarios por fila.
        Lanzar PluginError en caso de problemas.
        """
        pass

    @staticmethod
    @abstractmethod
    def detect(file_path: str) -> bool:
        """
        Retorna True si este plugin puede manejar el archivo.
        """
        pass
