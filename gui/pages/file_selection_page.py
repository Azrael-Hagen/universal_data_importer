from PySide6.QtWidgets import (
    QWizardPage,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QFormLayout,
    QMessageBox
)

import os

from core.format_detector import FormatDetector


class FileSelectionPage(QWizardPage):

    def __init__(self):

        super().__init__()

        self.setTitle("Seleccionar archivo")
        self.setSubTitle(
            "Seleccione el archivo que desea importar."
        )

        self.detector = FormatDetector()

        self.file_path = None
        self.detection_result = None

        self._build_ui()

    # =====================================================
    # UI
    # =====================================================

    def _build_ui(self):

        layout = QVBoxLayout()

        # -------------------------------
        # selector archivo
        # -------------------------------

        file_layout = QHBoxLayout()

        self.file_edit = QLineEdit()
        self.file_edit.setPlaceholderText("Seleccione un archivo...")

        browse_button = QPushButton("Examinar")

        browse_button.clicked.connect(self.browse_file)

        file_layout.addWidget(self.file_edit)
        file_layout.addWidget(browse_button)

        # -------------------------------
        # info archivo
        # -------------------------------

        info_group = QGroupBox("Información del archivo")

        info_layout = QFormLayout()

        self.format_label = QLabel("-")
        self.encoding_label = QLabel("-")
        self.delimiter_label = QLabel("-")
        self.size_label = QLabel("-")

        info_layout.addRow("Formato:", self.format_label)
        info_layout.addRow("Encoding:", self.encoding_label)
        info_layout.addRow("Delimitador:", self.delimiter_label)
        info_layout.addRow("Tamaño:", self.size_label)

        info_group.setLayout(info_layout)

        layout.addLayout(file_layout)
        layout.addWidget(info_group)

        self.setLayout(layout)

    # =====================================================
    # BROWSE FILE
    # =====================================================

    def browse_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo",
            "",
            "Todos los archivos (*.*)"
        )

        if not file_path:
            return

        self.file_path = file_path

        self.file_edit.setText(file_path)

        self.analyze_file()

    # =====================================================
    # ANALIZAR ARCHIVO
    # =====================================================

    def analyze_file(self):

        try:

            result = self.detector.detect(self.file_path)

            self.detection_result = result

            self.update_file_info()

            self.completeChanged.emit()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo analizar el archivo:\n{str(e)}"
            )

    # =====================================================
    # ACTUALIZAR UI
    # =====================================================

    def update_file_info(self):

        if not self.detection_result:
            return

        result = self.detection_result

        self.format_label.setText(str(result.format))

        self.encoding_label.setText(
            result.encoding if result.encoding else "-"
        )

        self.delimiter_label.setText(
            result.delimiter if result.delimiter else "-"
        )

        size = os.path.getsize(self.file_path)

        self.size_label.setText(self._format_size(size))

    # =====================================================
    # FORMAT SIZE
    # =====================================================

    def _format_size(self, size):

        for unit in ["B", "KB", "MB", "GB"]:

            if size < 1024:
                return f"{size:.2f} {unit}"

            size /= 1024

        return f"{size:.2f} TB"

    # =====================================================
    # WIZARD CONTROL
    # =====================================================

    def isComplete(self):

        return self.file_path is not None

    # =====================================================
    # PASAR DATOS AL WIZARD
    # =====================================================

    def validatePage(self):

        if not self.file_path:

            QMessageBox.warning(
                self,
                "Archivo requerido",
                "Debe seleccionar un archivo."
            )

            return False

        wizard = self.wizard()

        wizard.selected_file = self.file_path
        wizard.detection_result = self.detection_result

        return True