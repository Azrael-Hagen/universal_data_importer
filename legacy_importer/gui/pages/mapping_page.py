from gui.pages.mapping_page import MappingPage
from gui.pages.mapping_page import MappingTableModel
from gui.pages.mapping_page import ComboBoxDelegate
from core.engine import ImportEngine
from PySide6.QtWidgets import (
    QWizardPage,
    QVBoxLayout,
    QLabel,
    QTableView,
    QMessageBox,
    QComboBox,
    QStyledItemDelegate
)
from PySide6.QtCore import Qt, QAbstractTableModel

# =========================================================
# DELEGATE PARA COMBOBOX EN TABLEVIEW
# =========================================================
class ComboBoxDelegate(QStyledItemDelegate):
    """Permite seleccionar valores de un combo en QTableView."""

    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.items = items

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        combo.addItems(self.items)
        return combo

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        i = editor.findText(value)
        if i >= 0:
            editor.setCurrentIndex(i)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), Qt.EditRole)

# =========================================================
# MODELO PARA EL MAPPING
# =========================================================
class MappingTableModel(QAbstractTableModel):
    """Modelo para mapear columnas de origen a destino."""

    def __init__(self, source_columns, db_columns):
        super().__init__()
        self.source_columns = source_columns
        self.db_columns = [None] * len(source_columns)
        self.db_options = db_columns

    def rowCount(self, parent=None):
        return len(self.source_columns)

    def columnCount(self, parent=None):
        return 2  # Origen / Destino

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        row, col = index.row(), index.column()
        if role in (Qt.DisplayRole, Qt.EditRole):
            if col == 0:
                return self.source_columns[row]
            if col == 1:
                return self.db_columns[row] if self.db_columns[row] else ""
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False
        row, col = index.row(), index.column()
        if role == Qt.EditRole and col == 1:
            self.db_columns[row] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        if index.column() == 1:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return ["Source Column", "Database Column"][section]
            if orientation == Qt.Vertical:
                return str(section)
        return None

# =========================================================
# MAPPING PAGE
# =========================================================
class MappingPage(QWizardPage):
    """Página para mapear columnas del dataset a la base de datos."""

    def __init__(self):
        super().__init__()
        self.setTitle("Mapeo de columnas")
        self.setSubTitle("Mapee las columnas del dataset a las columnas de la base de datos.")
        self.model = None
        self.table = None
        self._build_ui()

    # =====================================================
    # UI
    # =====================================================
    def _build_ui(self):
        layout = QVBoxLayout()
        self.info_label = QLabel("Cargando mapeo...")
        self.table = QTableView()
        layout.addWidget(self.info_label)
        layout.addWidget(self.table)
        self.setLayout(layout)

    # =====================================================
    # CUANDO SE ENTRA A LA PÁGINA
    # =====================================================
    def initializePage(self):
        wizard = self.wizard()
        source_columns = getattr(wizard, "schema_columns", None)
        db_columns = getattr(wizard, "db_columns", None)

        if not source_columns or not db_columns:
            QMessageBox.critical(
                self,
                "Error",
                "No se definieron columnas de origen o destino para mapear"
            )
            return

        self.model = MappingTableModel(source_columns, db_columns)
        self.table.setModel(self.model)

        # Delegate para la columna de DB con combo box
        delegate = ComboBoxDelegate(db_columns, self.table)
        self.table.setItemDelegateForColumn(1, delegate)

        self.update_info()

    # =====================================================
    # INFO DEL MAPPING
    # =====================================================
    def update_info(self):
        rows = len(self.model.source_columns) if self.model else 0
        self.info_label.setText(f"Columnas a mapear: {rows}")

    # =====================================================
    # VALIDACIÓN
    # =====================================================
    def validatePage(self):
        """Guardar mapeo final en wizard para usarlo en ImportEngine."""
        wizard = self.wizard()
        if not self.model:
            return False
        # Diccionario source -> target
        wizard.mapping = [
            {"source": src, "target": tgt, "transform": None}
            for src, tgt in zip(self.model.source_columns, self.model.db_columns)
        ]
        return True
