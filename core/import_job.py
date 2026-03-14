from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ImportJob:
    file_path: Path
    plugin: Any
    schema: Any
    mapping: Any
    loader: Any
    config: Any
