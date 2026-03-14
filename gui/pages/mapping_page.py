"""
MappingPage

Allows mapping between source columns and destination columns.
This is a key ETL step before importing data.
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


TRANSFORM_OPTIONS = [
    "NONE",
    "TRIM",
    "LOWER",
    "UPPER",
    "INT",
    "FLOAT",
    "BOOLEAN",
    "DATE",
    "DATETIME",
    "JSON_PARSE",
]


class MappingPage(QWidget):
    """
    UI page used to map source columns to destination columns.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.source_columns = []
        self.target_schema = []

        self.init_ui()

    # --------------------------------------------------

    def init_ui(self):

        layout = QVBoxLayout()

        title = QLabel("Column Mapping")
        title.setStyleSheet("font-size:16px; font-weight:bold")

        layout.addWidget(title)

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels(
            [
                "Enabled",
                "Source Column",
                "Target Column",
                "Target Type",
                "Transform",
                "Notes",
            ]
        )

        self.table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()

        self.auto_map_btn = QPushButton("Auto Map")
        self.clear_btn = QPushButton("Clear Mapping")
        self.validate_btn = QPushButton("Validate Mapping")

        button_layout.addWidget(self.auto_map_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.validate_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    # --------------------------------------------------

    def load_mapping(self, source_columns, schema):

        """
        Populate mapping table using source columns and detected schema.
        """

        self.source_columns = source_columns
        self.target_schema = schema.get("columns", [])

        self.table.setRowCount(len(source_columns))

        target_names = [c["target_name"] if "target_name" in c else c["name"] for c in self.target_schema]
        target_types = {c.get("target_name", c["name"]): c["type"] for c in self.target_schema}

        for row, source in enumerate(source_columns):

            # Enabled
            enabled = QCheckBox()
            enabled.setChecked(True)

            self.table.setCellWidget(row, 0, enabled)

            # Source column
            src_item = QTableWidgetItem(source)
            src_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            self.table.setItem(row, 1, src_item)

            # Target column selector
            target_combo = QComboBox()
            target_combo.addItems([""] + target_names)

            self.table.setCellWidget(row, 2, target_combo)

            # Target type
            type_combo = QComboBox()

            type_combo.addItems(
                [
                    "INTEGER",
                    "FLOAT",
                    "BOOLEAN",
                    "TEXT",
                    "DATE",
                    "DATETIME",
                    "JSON",
                    "BLOB",
                ]
            )

            self.table.setCellWidget(row, 3, type_combo)

            # Transform
            transform_combo = QComboBox()
            transform_combo.addItems(TRANSFORM_OPTIONS)

            self.table.setCellWidget(row, 4, transform_combo)

            # Notes
            notes_item = QTableWidgetItem("")
            notes_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            self.table.setItem(row, 5, notes_item)

    # --------------------------------------------------

    def auto_map(self):
        """
        Attempt automatic mapping by matching column names.
        """

        for row in range(self.table.rowCount()):

            source = self.table.item(row, 1).text().lower()

            combo = self.table.cellWidget(row, 2)

            for i in range(combo.count()):

                target = combo.itemText(i).lower()

                if source == target:
                    combo.setCurrentIndex(i)
                    break

    # --------------------------------------------------

    def clear_mapping(self):

        """
        Remove all mappings.
        """

        for row in range(self.table.rowCount()):

            combo = self.table.cellWidget(row, 2)
            combo.setCurrentIndex(0)

    # --------------------------------------------------

    def validate_mapping(self):

        """
        Validate mapping and add notes.
        """

        used_targets = set()

        for row in range(self.table.rowCount()):

            notes = []

            enabled = self.table.cellWidget(row, 0).isChecked()

            if not enabled:
                continue

            source = self.table.item(row, 1).text()

            target_combo = self.table.cellWidget(row, 2)
            target = target_combo.currentText()

            if not target:
                notes.append("No target column")

            if target in used_targets:
                notes.append("Duplicate target")

            used_targets.add(target)

            notes_item = self.table.item(row, 5)

            notes_item.setText(", ".join(notes))

    # --------------------------------------------------

    def get_mapping(self):

        """
        Extract mapping configuration from UI.
        """

        mapping = []

        for row in range(self.table.rowCount()):

            enabled = self.table.cellWidget(row, 0).isChecked()

            if not enabled:
                continue

            source = self.table.item(row, 1).text()

            target = self.table.cellWidget(row, 2).currentText()

            dtype = self.table.cellWidget(row, 3).currentText()

            transform = self.table.cellWidget(row, 4).currentText()

            mapping.append(
                {
                    "source": source,
                    "target": target,
                    "type": dtype,
                    "transform": transform,
                }
            )

        return mapping