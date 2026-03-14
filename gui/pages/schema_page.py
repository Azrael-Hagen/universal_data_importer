"""
SchemaPage

Allows the user to review and edit the detected schema before import.

Features
--------
- Editable table schema
- Change column names
- Modify data types
- Set primary keys
- Enable/disable columns
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QCheckBox,
    QPushButton,
    QHBoxLayout,
)

from PySide6.QtCore import Qt


SUPPORTED_TYPES = [
    "INTEGER",
    "FLOAT",
    "BOOLEAN",
    "TEXT",
    "DATE",
    "DATETIME",
    "JSON",
    "BLOB",
]


class SchemaPage(QWidget):
    """
    Page used to inspect and modify detected schema.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.schema = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Review and edit detected schema")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels(
            [
                "Enabled",
                "Source Name",
                "Target Name",
                "Type",
                "Primary Key",
                "Nullable",
                "Sample",
            ]
        )

        self.table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()

        self.redetect_btn = QPushButton("Re-detect schema")
        self.auto_types_btn = QPushButton("Auto detect types")
        self.guess_pk_btn = QPushButton("Guess Primary Key")
        self.reset_btn = QPushButton("Reset")

        button_layout.addWidget(self.redetect_btn)
        button_layout.addWidget(self.auto_types_btn)
        button_layout.addWidget(self.guess_pk_btn)
        button_layout.addWidget(self.reset_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    # --------------------------------------------------

    def load_schema(self, schema):
        """
        Populate table with schema information.
        """

        self.schema = schema

        columns = schema.get("columns", [])

        self.table.setRowCount(len(columns))

        for row, col in enumerate(columns):

            # Enabled checkbox
            enabled = QCheckBox()
            enabled.setChecked(True)
            self.table.setCellWidget(row, 0, enabled)

            # Source name
            source_item = QTableWidgetItem(col.get("name", ""))
            source_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(row, 1, source_item)

            # Target name (editable)
            target_item = QTableWidgetItem(col.get("name", ""))
            self.table.setItem(row, 2, target_item)

            # Type selector
            type_combo = QComboBox()
            type_combo.addItems(SUPPORTED_TYPES)

            detected = col.get("type", "TEXT")

            if detected in SUPPORTED_TYPES:
                type_combo.setCurrentText(detected)

            self.table.setCellWidget(row, 3, type_combo)

            # Primary key
            pk_checkbox = QCheckBox()
            pk_checkbox.setChecked(col.get("primary_key", False))
            self.table.setCellWidget(row, 4, pk_checkbox)

            # Nullable
            nullable_checkbox = QCheckBox()
            nullable_checkbox.setChecked(col.get("nullable", True))
            self.table.setCellWidget(row, 5, nullable_checkbox)

            # Sample value
            sample = col.get("sample", "")
            sample_item = QTableWidgetItem(str(sample))
            sample_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(row, 6, sample_item)

    # --------------------------------------------------

    def get_schema(self):
        """
        Extract schema configuration from UI.
        """

        columns = []

        for row in range(self.table.rowCount()):

            enabled = self.table.cellWidget(row, 0).isChecked()

            if not enabled:
                continue

            source_name = self.table.item(row, 1).text()
            target_name = self.table.item(row, 2).text()

            type_combo = self.table.cellWidget(row, 3)
            dtype = type_combo.currentText()

            pk = self.table.cellWidget(row, 4).isChecked()
            nullable = self.table.cellWidget(row, 5).isChecked()

            columns.append(
                {
                    "source_name": source_name,
                    "target_name": target_name,
                    "type": dtype,
                    "primary_key": pk,
                    "nullable": nullable,
                }
            )

        return {
            "columns": columns
        }

    # --------------------------------------------------

    def reset(self):
        """
        Reset UI to original detected schema.
        """

        if self.schema:
            self.load_schema(self.schema)