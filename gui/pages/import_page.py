from PySide6.QtWidgets import (
    QWizardPage,
    QVBoxLayout,
    QLabel,
    QProgressBar,
    QTextEdit,
    QMessageBox
)
from PySide6.QtCore import Qt, QTimer, Slot
from core.engine import ImportEngine

# =========================================================
# IMPORT PAGE
# =========================================================
class ImportPage(QWizardPage):
    """Página para ejecutar la importación de datos."""

    def __init__(self):
        super().__init__()
        self.setTitle("Importación de datos")
        self.setSubTitle("Se procesarán los datos hacia la base de datos seleccionada.")

        self.progress_bar = None
        self.log_view = None
        self.engine = None
        self._build_ui()

    # =====================================================
    # UI
    # =====================================================
    def _build_ui(self):
        layout = QVBoxLayout()

        self.info_label = QLabel("Preparado para iniciar la importación...")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)

        layout.addWidget(self.info_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.log_view)

        self.setLayout(layout)

    # =====================================================
    # CUANDO SE ENTRA A LA PÁGINA
    # =====================================================
    def initializePage(self):
        wizard = self.wizard()
        self.engine = ImportEngine(
            state={
                "file_path": getattr(wizard, "selected_file", ""),
                "format": getattr(wizard, "detection_result", {}).get("format", ""),
                "schema": getattr(wizard, "schema_columns", []),
                "mapping": getattr(wizard, "mapping", [])
            },
            progress_callback=self.update_progress,
            log_callback=self.append_log
        )

        # Ejecutar import con un delay mínimo para que QWizard cargue la UI
        QTimer.singleShot(100, self.run_import)

    # =====================================================
    # ACTUALIZAR PROGRESO
    # =====================================================
    @Slot(int)
    def update_progress(self, percent: int):
        self.progress_bar.setValue(percent)

    # =====================================================
    # LOGS
    # =====================================================
    @Slot(str)
    def append_log(self, message: str):
        self.log_view.append(message)

    # =====================================================
    # EJECUTAR IMPORT
    # =====================================================
    def run_import(self):
        try:
            rows, errors = self.engine.run()
            self.append_log(f"Importación finalizada: {rows} filas procesadas, {errors} errores.")
            QMessageBox.information(
                self,
                "Importación completada",
                f"Se procesaron {rows} filas.\nErrores: {errors}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error en importación",
                f"Ocurrió un error durante la importación:\n{str(e)}"
            )
            self.append_log(f"Error crítico: {str(e)}")
