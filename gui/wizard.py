"""
Wizard controller for Universal Data Importer GUI.

This module coordinates the navigation and data flow
between all wizard pages.
"""

from PySide6.QtWidgets import (
    QWizard,
)

from gui.pages.file_select_page import FileSelectPage
from gui.pages.preview_page import PreviewPage
from gui.pages.schema_page import SchemaPage
from gui.pages.mapping_page import MappingPage
from gui.pages.import_page import ImportPage

from core.format_detector import detect_format
from core.schema_detector import SchemaDetector

import pandas as pd
from config.settings import PREVIEW_ROWS, BATCH_SIZE, SQLITE_DB_PATH, DEFAULT_TABLE_NAME


class ImportWizard(QWizard):

    PAGE_FILE = 0
    PAGE_PREVIEW = 1
    PAGE_SCHEMA = 2
    PAGE_MAPPING = 3
    PAGE_IMPORT = 4

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Universal Data Importer")

        self.resize(900, 600)

        # State shared across pages
        self.state = {
            "file_path": None,
            "format": None,
            "preview_data": None,
            "schema": None,
            "mapping": None,
        }

        self.init_pages()

        self.currentIdChanged.connect(self.on_page_changed)

    # --------------------------------------------------

    def init_pages(self):

        self.file_page = FileSelectPage()
        self.preview_page = PreviewPage()
        self.schema_page = SchemaPage()
        self.mapping_page = MappingPage()
        self.import_page = ImportPage()

       
        self.addPage(self.file_page)
        self.addPage(self.preview_page)
        self.addPage(self.schema_page)
        self.addPage(self.mapping_page)
        self.addPage(self.import_page)

    # --------------------------------------------------

    def on_page_changed(self, page_id):

        if page_id == self.PAGE_PREVIEW:
            self.prepare_preview()

        elif page_id == self.PAGE_SCHEMA:
            self.prepare_schema()

        elif page_id == self.PAGE_MAPPING:
            self.prepare_mapping()
        elif page_id == self.PAGE_IMPORT:
            self.prepare_import()

    # --------------------------------------------------

    def prepare_preview(self):

        file_path = self.file_page.get_file_path()

        if not file_path:
            return

        self.state["file_path"] = file_path

        file_format = detect_format(file_path)

        self.state["format"] = file_format

        df = self.load_preview(file_path, file_format)

        self.state["preview_data"] = df

        self.preview_page.load_dataframe(df)

    # --------------------------------------------------

    def load_preview(self, file_path, file_format):

        """
        Load small preview dataset depending on format.
        """

        if file_format == "csv":

            return pd.read_csv(file_path, nrows=PREVIEW_ROWS)

        if file_format == "excel":

            return pd.read_excel(file_path, nrows=PREVIEW_ROWS)

        if file_format == "json":

            return pd.read_json(file_path)

        if file_format == "xml":

            return pd.read_xml(file_path)

        raise ValueError(f"Unsupported preview format: {file_format}")

    # --------------------------------------------------

    def prepare_schema(self):

        df = self.state.get("preview_data")

        if df is None:
            return

        detector = SchemaDetector()

        schema = detector.detect_from_dataframe(df)

        self.state["schema"] = schema

        self.schema_page.load_schema(schema)

    # --------------------------------------------------

    def prepare_mapping(self):

        df = self.state.get("preview_data")
        schema = self.schema_page.get_schema()

        if df is None:
            return

        source_columns = list(df.columns)

        self.mapping_page.load_mapping(source_columns, schema)

    # --------------------------------------------------

    def prepare_import(self):

        mapping = self.mapping_page.get_mapping()
        schema = self.schema_page.get_schema()

        self.state["mapping"] = mapping
        self.state["schema"] = schema

        self.import_page.set_state(self.state)
        
    #---------------------------------------------------
    def accept(self):

        """
        Called when wizard finishes.
        """

        mapping = self.mapping_page.get_mapping()

        self.state["mapping"] = mapping

        print("Import configuration:")
        print(self.state)

        super().accept()