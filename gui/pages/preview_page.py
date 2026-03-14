from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QTableWidget,
    QTableWidgetItem, QMessageBox
)
from PySide6.QtCore import Signal, Qt
from plugins.plugin_registry import PluginRegistry
from core.exceptions import PluginError
import pandas as pd

class PreviewPage(QWidget):
    """
    Página genérica de preview de datos.
    Independiente de wizard, reutilizable y escalable.
    """

    # Señal emitida cuando el preview está listo
    preview_ready = Signal(object)  # dict: {'plugin': plugin_instance, 'df': dataframe}

    def __init__(self, parent=None, preview_rows: int = 10):
        super().__init__(parent)
        self.preview_rows = preview_rows
        self.plugin = None
        self.df = pd.DataFrame()

        # Layout
        self.layout = QVBoxLayout(self)

        # Botón para seleccionar archivo
        self.select_button = QPushButton("Seleccionar archivo")
        self.select_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.select_button)

        # Label de info
        self.info_label = QLabel("No hay archivo seleccionado")
        self.layout.addWidget(self.info_label)

        # Tabla para mostrar preview
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

    # -----------------------------------------
    # Abrir diálogo de archivo
    # -----------------------------------------
    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo",
            "",
            "Todos los archivos (*.*)"
        )
        if file_path:
            self.load_file(file_path)

    # -----------------------------------------
    # Cargar archivo usando plugin
    # -----------------------------------------
    def load_file(self, file_path: str):
        self.info_label.setText(f"Cargando: {file_path}")
        try:
            # Detectar plugin automáticamente
            plugin_cls = PluginRegistry.detect_plugin(file_path)
            if not plugin_cls:
                raise PluginError("No se pudo detectar un plugin para este archivo")

            # Crear instancia del plugin
            self.plugin = plugin_cls(file_path)

            # Leer preview de primeras N filas
            rows = []
            for i, row in enumerate(self.plugin.read_rows()):
                rows.append(row)
                if i >= self.preview_rows - 1:
                    break

            if not rows:
                raise PluginError("Archivo vacío o sin filas legibles")

            # Convertir a dataframe
            self.df = pd.DataFrame(rows)

            # Mostrar en tabla
            self.show_preview_table()

            self.info_label.setText(f"{len(self.df)} filas cargadas")

            # Emitir señal
            self.preview_ready.emit({'plugin': self.plugin, 'df': self.df})

        except PluginError as e:
            QMessageBox.critical(self, "Error plugin", str(e))
            self.info_label.setText("Error cargando archivo")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.info_label.setText("Error inesperado")

    # -----------------------------------------
    # Mostrar tabla con preview
    # -----------------------------------------
    def show_preview_table(self):
        if self.df.empty:
            return

        headers = list(self.df.columns)
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(self.df))
        self.table.setHorizontalHeaderLabels(headers)

        for i, row in self.df.iterrows():
            for j, key in enumerate(headers):
                item = QTableWidgetItem(str(row[key]))
                item.setFlags(Qt.ItemIsEnabled)  # Solo lectura
                self.table.setItem(i, j, item)
