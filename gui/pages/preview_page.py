from PySide6.QtWidgets import (
    QWizardPage,
    QVBoxLayout,
    QLabel,
    QTableView,
    QMessageBox
)

from PySide6.QtCore import Qt, QAbstractTableModel

import pandas as pd


# =========================================================
# MODELO PARA PANDAS
# =========================================================

class PandasTableModel(QAbstractTableModel):

    def __init__(self, dataframe):

        super().__init__()

        self.df = dataframe

    def rowCount(self, parent=None):

        return len(self.df)

    def columnCount(self, parent=None):

        return len(self.df.columns)

    def data(self, index, role=Qt.DisplayRole):

        if role == Qt.DisplayRole:

            value = self.df.iloc[index.row(), index.column()]

            return str(value)

        return None

    def headerData(self, section, orientation, role):

        if role == Qt.DisplayRole:

            if orientation == Qt.Horizontal:
                return str(self.df.columns[section])

            if orientation == Qt.Vertical:
                return str(section)

        return None


# =========================================================
# PREVIEW PAGE
# =========================================================

class PreviewPage(QWizardPage):

    PREVIEW_ROWS = 100

    def __init__(self):

        super().__init__()

        self.setTitle("Vista previa de datos")
        self.setSubTitle(
            "Revise una muestra de los datos antes de continuar."
        )

        self.df = None

        self._build_ui()

    # =====================================================
    # UI
    # =====================================================

    def _build_ui(self):

        layout = QVBoxLayout()

        self.info_label = QLabel("Cargando datos...")

        self.table = QTableView()

        layout.addWidget(self.info_label)
        layout.addWidget(self.table)

        self.setLayout(layout)

    # =====================================================
    # CUANDO SE ENTRA A LA PÁGINA
    # =====================================================

    def initializePage(self):

        wizard = self.wizard()

        file_path = wizard.selected_file
        detection = wizard.detection_result

        try:

            self.df = self.load_preview(file_path, detection)

            model = PandasTableModel(self.df)

            self.table.setModel(model)

            self.update_info()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo cargar la vista previa:\n{str(e)}"
            )

    # =====================================================
    # CARGAR PREVIEW
    # =====================================================

    def load_preview(self, file_path, detection):

        fmt = detection.format

        if fmt == "csv":

            return pd.read_csv(
                file_path,
                encoding=detection.encoding,
                delimiter=detection.delimiter,
                nrows=self.PREVIEW_ROWS
            )

        if fmt == "excel":

            return pd.read_excel(
                file_path,
                nrows=self.PREVIEW_ROWS
            )

        if fmt == "json":

            df = pd.read_json(file_path)

            return df.head(self.PREVIEW_ROWS)

        raise Exception(f"Formato no soportado aún: {fmt}")

    # =====================================================
    # INFO DATASET
    # =====================================================

    def update_info(self):

        rows = len(self.df)
        cols = len(self.df.columns)

        self.info_label.setText(
            f"Filas mostradas: {rows} | Columnas: {cols}"
        )

    # =====================================================
    # VALIDACIÓN
    # =====================================================

    def validatePage(self):

        wizard = self.wizard()

        wizard.preview_df = self.df

        return True