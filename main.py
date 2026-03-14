import sys
from PySide6.QtWidgets import QApplication, QWizard, QFileDialog, QMessageBox

from gui.pages.preview_page import PreviewPage
from gui.pages.schema_page import SchemaPage
from gui.pages.mapping_page import MappingPage
from gui.pages.import_page import ImportPage

# =========================================================
# MAIN WIZARD
# =========================================================
class UniversalDataImporterWizard(QWizard):
    """Wizard principal que integra todas las páginas para importar datos."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Universal Data Importer")

        # Atributos compartidos entre páginas
        self.selected_file = None
        self.detection_result = {}  # formate, delimiter, encoding
        self.preview_df = None
        self.schema_columns = []
        self.schema_types = []
        self.db_columns = []  # columnas disponibles en la base de datos
        self.mapping = []

        # Configurar páginas
        self._setup_pages()

        # Selección inicial de archivo
        if not self.select_file():
            QMessageBox.critical(self, "Error", "No se seleccionó ningún archivo. Saliendo...")
            sys.exit(0)

    # =====================================================
    # CONFIGURAR PÁGINAS
    # =====================================================
    def _setup_pages(self):
        self.preview_page = PreviewPage()
        self.schema_page = SchemaPage()
        self.mapping_page = MappingPage()
        self.import_page = ImportPage()

        self.addPage(self.preview_page)
        self.addPage(self.schema_page)
        self.addPage(self.mapping_page)
        self.addPage(self.import_page)

    # =====================================================
    # SELECCIÓN DE ARCHIVO
    # =====================================================
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccione el archivo a importar",
            "",
            "Todos los archivos (*.*);;CSV (*.csv);;Excel (*.xlsx *.xls);;JSON (*.json);;XML (*.xml)"
        )
        if not file_path:
            return False

        self.selected_file = file_path

        # Detectar formato automáticamente (puedes integrar tu plugin de detection)
        self._detect_file_format()
        return True

    # =====================================================
    # DETECCIÓN DE FORMATO SIMPLE
    # =====================================================
    def _detect_file_format(self):
        ext = self.selected_file.split(".")[-1].lower()
        self.detection_result = {
            "format": "csv" if ext in ["csv"] else
                      "excel" if ext in ["xls", "xlsx"] else
                      "json" if ext in ["json"] else
                      "xml" if ext in ["xml"] else None,
            "delimiter": ",",
            "encoding": "utf-8"
        }
        if self.detection_result["format"] is None:
            QMessageBox.warning(self, "Formato no soportado", f"No se reconoce la extensión: {ext}")

        # Para demo, simular columnas de DB
        self.db_columns = ["col1", "col2", "col3", "col4", "col5"]

# =========================================================
# EJECUTAR APP
# =========================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    wizard = UniversalDataImporterWizard()
    wizard.show()
    sys.exit(app.exec())
