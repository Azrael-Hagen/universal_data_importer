from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


FILES = {
    "core/models.py": '''
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ColumnInfo:
    name: str
    dtype: str
    nullable: bool = True
    sample_values: List[Any] = field(default_factory=list)


@dataclass
class Schema:
    columns: List[ColumnInfo]


@dataclass
class Mapping:
    source_column: str
    target_column: str


@dataclass
class ImportConfig:
    table_name: str
    mappings: List[Mapping]
    create_table: bool = True
''',

    "core/exceptions.py": '''
class ImporterError(Exception):
    """Base exception for the importer."""


class UnsupportedFormatError(ImporterError):
    pass


class SchemaDetectionError(ImporterError):
    pass


class DatabaseConnectionError(ImporterError):
    pass


class ImportExecutionError(ImporterError):
    pass
''',

    "core/import_job.py": '''
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
''',

    "plugins/base_plugin.py": '''
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
''',

    "plugins/plugin_registry.py": '''
from plugins.csv_plugin import CSVPlugin
from plugins.json_plugin import JSONPlugin
from plugins.excel_plugin import ExcelPlugin
from plugins.xml_plugin import XMLPlugin


PLUGINS = [
    CSVPlugin(),
    JSONPlugin(),
    ExcelPlugin(),
    XMLPlugin()
]


def detect_plugin(file_path):
    for plugin in PLUGINS:
        if plugin.detect(file_path):
            return plugin
    return None
''',

    "loaders/loader_registry.py": '''
from loaders.sqlite_loader import SQLiteLoader
from loaders.mysql_loader import MySQLLoader
from loaders.postgres_loader import PostgresLoader


LOADERS = {
    "sqlite": SQLiteLoader,
    "mysql": MySQLLoader,
    "postgres": PostgresLoader
}


def get_loader(loader_type: str):
    return LOADERS.get(loader_type)
''',

    "utils/progress.py": '''
class ProgressTracker:

    def __init__(self):
        self.current = 0
        self.total = 0

    def start(self, total: int):
        self.total = total
        self.current = 0

    def update(self, step: int = 1):
        self.current += step

    def percent(self):
        if self.total == 0:
            return 0
        return (self.current / self.total) * 100
''',

    "gui/dialogs/db_connection_dialog.py": '''
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox
)


class DBConnectionDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Database Connection")

        layout = QVBoxLayout()

        self.db_type = QComboBox()
        self.db_type.addItems(["sqlite", "mysql", "postgres"])

        self.host = QLineEdit()
        self.host.setPlaceholderText("Host")

        self.database = QLineEdit()
        self.database.setPlaceholderText("Database")

        self.user = QLineEdit()
        self.user.setPlaceholderText("User")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")

        self.connect_btn = QPushButton("Connect")

        layout.addWidget(QLabel("Database Type"))
        layout.addWidget(self.db_type)

        layout.addWidget(self.host)
        layout.addWidget(self.database)
        layout.addWidget(self.user)
        layout.addWidget(self.password)

        layout.addWidget(self.connect_btn)

        self.setLayout(layout)
'''
}


def create_file(path: Path, content: str):
    if path.exists():
        print(f"Skipping existing file: {path}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(content.strip() + "\n", encoding="utf-8")

    print(f"Created: {path}")


def main():
    print("Bootstrapping project architecture...\n")

    for relative_path, content in FILES.items():
        full_path = PROJECT_ROOT / relative_path
        create_file(full_path, content)

    print("\nBootstrap complete.")


if __name__ == "__main__":
    main()