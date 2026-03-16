from pathlib import Path
from typing import Dict, Optional


class DataSource:
    """
    Represents a data source used in a pipeline.

    This can be:
    - File
    - Database
    - API
    - Stream
    """

    def __init__(
        self,
        path: str,
        file_type: str,
        metadata: Optional[Dict] = None,
        config: Optional[Dict] = None
    ):
        self.path = path
        self.file_type = file_type
        self.metadata = metadata or {}
        self.config = config or {}

    # -----------------------------------------
    # File utilities
    # -----------------------------------------

    def exists(self) -> bool:
        """
        Check if the source exists (for files).
        """

        return Path(self.path).exists()

    def filename(self) -> str:
        """
        Return filename.
        """

        return Path(self.path).name

    def extension(self) -> str:
        """
        Return file extension.
        """

        return Path(self.path).suffix

    # -----------------------------------------
    # Serialization
    # -----------------------------------------

    def to_dict(self):

        return {
            "path": self.path,
            "file_type": self.file_type,
            "metadata": self.metadata,
            "config": self.config,
        }

    # -----------------------------------------
    # Representation
    # -----------------------------------------

    def describe(self) -> str:

        return (
            f"DataSource:\n"
            f"  Path: {self.path}\n"
            f"  Type: {self.file_type}"
        )

    def __repr__(self):

        return f"<DataSource {self.file_type}: {self.path}>"