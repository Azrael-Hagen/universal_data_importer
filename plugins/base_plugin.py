from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from core.models import Schema


class BasePlugin(ABC):
    """
    Base class for all file format plugins.
    """

    name: str = "base"

    # --------------------------------------------------
    # Format detection
    # --------------------------------------------------

    @abstractmethod
    def detect(self, file_path: Path) -> bool:
        """
        Determine if this plugin can handle the file.
        """
        pass

    # --------------------------------------------------
    # Preview loading
    # --------------------------------------------------

    @abstractmethod
    def read_preview(self, file_path: Path, rows: int = 100) -> Any:
        """
        Load a preview of the dataset.

        Returns:
            Typically a pandas DataFrame or list of dicts.
        """
        pass

    # --------------------------------------------------
    # Full dataset loading
    # --------------------------------------------------

    @abstractmethod
    def read_full(self, file_path: Path) -> Any:
        """
        Load the entire dataset.
        """
        pass

    # --------------------------------------------------
    # Schema detection
    # --------------------------------------------------

    @abstractmethod
    def detect_schema(self, data: Any) -> Schema:
        """
        Infer the dataset schema.
        """
        pass

    # --------------------------------------------------
    # Optional metadata
    # --------------------------------------------------

    def supported_extensions(self):

        """
        Returns supported file extensions.

        Example:
        ['.csv']
        """

        return []

    # --------------------------------------------------
    # Optional validation
    # --------------------------------------------------

    def validate(self, file_path: Path) -> bool:
        """
        Optional file validation before reading.
        """
        return True
