from abc import ABC, abstractmethod
from pathlib import Path


class BasePlugin(ABC):

    name = "base"

    @abstractmethod
    def detect(self, file_path: Path) -> bool:
        pass

    @abstractmethod
    def read_preview(self, file_path: Path, rows: int = 100):
        pass

    @abstractmethod
    def read_full(self, file_path: Path):
        pass

    @abstractmethod
    def detect_schema(self, data):
        pass
