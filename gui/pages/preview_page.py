from gui.pages.schema_page import SchemaPage
from gui.pages.preview_page import SchemaTableModel
from core.models import Schema
from PySide6.QtWidgets import (
    QWizardPage,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableView,
    QPushButton,
    QMessageBox,
    QComboBox
)
from PySide6.QtCore import Qt, QAbstractTableModel
import pandas as pd

# =========================================================
# MODELO PARA EDITAR SCHEMA
# =========================================================
class SchemaTableModel(QAbstractTableModel):
    """Modelo QTableView para edición de esquema de columnas."""

    SUPPORTED_TYPES = ["string", "int", "float", "bool"]

    def __init__(self, dataframe: pd.DataFrame):
        super().__init__()
        self.columns = list(dataframe.columns)
        # Default: inferir tipos básicos
        self.types = [self._infer_type(dataframe[col]) for col in self.columns]

    def rowCount(self, parent=None):
        return len(self.columns)

    def columnCount(self, parent=None):
        return 2  # Nombre y Tipo

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        row, col = index.row(), index.column()
        if role == Qt.DisplayRole or role == Qt.EditRole:
            if col == 0:
                return self.columns[row]
            if col == 1:
                return self.types[row]
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False
        row, col = index.row(), index.column()
        if role == Qt.EditRole:
            if col == 0:
                self.columns[row] = str(value)
            elif col == 1 and value in self.SUPPORTED_TYPES:
                self.types[row] = value
            else:
                return False
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return ["Column Name", "Type"][section]
            if orientation == Qt.Vertical:
                return str(section)
        return None

    def _infer_type(self, series: pd.Series):
        if pd.api.types.is_integer_dtype(series):
            return "int"
        elif pd.api.types.is_float_dtype(series):
            return "float"
        elif pd.api.types.is_bool_dtype(series):
            return "bool"
        else:
            return "string"

# =========================================================
# SCHEMA PAGE
# =========================================================
class SchemaPage(QWizardPage):
    """Página para revisión y edición del esquema de columnas."""

    def __init__(self):
        super().__init__()
        self.setTitle("Definir esquema")
        self.setSubTitle("Revise y modifique los nombres y tipos de las columnas.")
        self.df = None
        self.model = None
        self._build_ui()

    # =====================================================
    # UI
    # =====================================================
    def _build_ui(self):
        layout = QVBoxLayout()
        self.info_label = QLabel("Cargando esquema...")
        self.table = QTableView()
        layout.addWidget(self.info_label)
        layout.addWidget(self.table)
        self.setLayout(layout)

    # =====================================================
    # CUANDO SE ENTRA A LA PÁGINA
    # =====================================================
    def initializePage(self):
        wizard = self.wizard()
        self.df = getattr(wizard, "preview_df", None)
        if self.df is None or self.df.empty:
            QMessageBox.critical(self, "Error", "No hay datos de preview para definir esquema")
            self.df = pd.DataFrame()
            return

        self.model = SchemaTableModel(self.df)
        self.table.setModel(self.model)
        self.update_info()

    # =====================================================
    # INFO DEL SCHEMA
    # =====================================================
    def update_info(self):
        rows = len(self.model.columns) if self.model else 0
        self.info_label.setText(f"Columnas: {rows}")

    # =====================================================
    # VALIDACIÓN
    # =====================================================
    def validatePage(self):
        """Guarda el esquema editado en el wizard para usarlo en mapping y engine."""
        wizard = self.wizard()
        if not self.model:
            return False
        wizard.schema_columns = self.model.columns
        wizard.schema_types = self.model.types
        return True
