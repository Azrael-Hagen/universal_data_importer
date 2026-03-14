from pathlib import Path
from typing import Any, List

from plugins.plugin_registry import detect_plugin
from loaders.loader_registry import get_loader

from core.exceptions import (
    UnsupportedFormatError,
    ImportExecutionError,
)

from utils.logger import get_logger

logger = get_logger(__name__)


class ImportEngine:

    def __init__(self):
        self.plugin = None
        self.schema = None

    # -----------------------------------
    # Detect file format
    # -----------------------------------

    def detect_format(self, file_path: Path):

        logger.info(f"Detecting format for {file_path}")

        plugin = detect_plugin(file_path)

        if not plugin:
            raise UnsupportedFormatError(
                f"Unsupported file format: {file_path}"
            )

        self.plugin = plugin

        logger.info(f"Detected plugin: {plugin.name}")

        return plugin.name

    # -----------------------------------
    # Load preview
    # -----------------------------------

    def load_preview(self, file_path: Path, rows: int = 100):

        if not self.plugin:
            self.detect_format(file_path)

        logger.info("Loading preview")

        preview = self.plugin.read_preview(file_path, rows)

        return preview

    # -----------------------------------
    # Detect schema
    # -----------------------------------

    def detect_schema(self, preview_data):

        if not self.plugin:
            raise RuntimeError("Plugin not initialized")

        logger.info("Detecting schema")

        schema = self.plugin.detect_schema(preview_data)

        self.schema = schema

        return schema

    # -----------------------------------
    # Run import
    # -----------------------------------

    def run_import(
        self,
        file_path: Path,
        loader_type: str,
        connection_config: dict,
        table_name: str,
        mapping: List[dict],
    ):

        try:

            if not self.plugin:
                self.detect_format(file_path)

            logger.info("Reading full dataset")

            data = self.plugin.read_full(file_path)

            loader_class = get_loader(loader_type)

            if not loader_class:
                raise ImportExecutionError(
                    f"Unknown loader: {loader_type}"
                )

            loader = loader_class(connection_config)

            logger.info("Executing import")

            loader.load_data(
                data=data,
                table_name=table_name,
                mapping=mapping,
            )

            logger.info("Import completed")

        except Exception as e:

            logger.exception("Import failed")

            raise ImportExecutionError(str(e)) from e