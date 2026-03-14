"""
ImportPage

Final step of the wizard.
Responsible for running the data import process
and displaying progress, logs and statistics.
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QProgressBar,
    QTextEdit,
    QHBoxLayout,
)

from PySide6.QtCore import QThread, Signal

class ImportWorker(QThread):
    """
    Worker thread used to run the import process
    without freezing the GUI.
    """

    progress = Signal(int)
    log = Signal(str)
    finished = Signal()
    stats = Signal(int, int)

    def __init__(self, state):
        super().__init__()

        self.state = state
        self.running = True

    def stop(self):
        self.running = False

    def run(self):

        """
        Placeholder import logic.
        Later this will call core.engine
        """

        import time

        from core.engine import ImportEngine

        rows = 100
        processed = 0
        errors = 0
#----------------------------------------------------------------------
        engine = ImportEngine(
            self.state,
            progress_callback=self.progress.emit,
            log_callback=self.log.emit,
        )

        rows, errors = engine.run()

        self.stats.emit(rows, errors)
#----------------------------------------------------------------------
        self.log.emit("Starting import...")

        for i in range(rows):

            if not self.running:
                self.log.emit("Import cancelled")
                break

            time.sleep(0.03)

            processed += 1

            percent = int((processed / rows) * 100)

            self.progress.emit(percent)

            if i % 10 == 0:
                self.log.emit(f"Processed {processed} rows")

        self.stats.emit(processed, errors)

        self.log.emit("Import finished")

        self.finished.emit()


class ImportPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.state = None
        self.worker = None

        self.init_ui()

    # --------------------------------------------------

    def init_ui(self):

        layout = QVBoxLayout()

        title = QLabel("Import Data")
        title.setStyleSheet("font-size:16px; font-weight:bold")

        layout.addWidget(title)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        layout.addWidget(self.progress_bar)

        # Stats
        self.stats_label = QLabel("Rows processed: 0 | Errors: 0")

        layout.addWidget(self.stats_label)

        # Log window
        self.log_window = QTextEdit()
        self.log_window.setReadOnly(True)

        layout.addWidget(self.log_window)

        # Buttons
        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start Import")
        self.cancel_button = QPushButton("Cancel")

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Signals
        self.start_button.clicked.connect(self.start_import)
        self.cancel_button.clicked.connect(self.cancel_import)

    # --------------------------------------------------

    def set_state(self, state):
        """
        Receive wizard state.
        """

        self.state = state

    # --------------------------------------------------

    def start_import(self):

        if not self.state:
            self.log("No import configuration")
            return

        self.progress_bar.setValue(0)
        self.log_window.clear()

        self.worker = ImportWorker(self.state)

        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.log.connect(self.log)
        self.worker.finished.connect(self.import_finished)
        self.worker.stats.connect(self.update_stats)

        self.worker.start()

    # --------------------------------------------------

    def cancel_import(self):

        if self.worker:
            self.worker.stop()

    # --------------------------------------------------

    def import_finished(self):

        self.log("Import process completed")

    # --------------------------------------------------

    def update_stats(self, rows, errors):

        self.stats_label.setText(
            f"Rows processed: {rows} | Errors: {errors}"
        )

    # --------------------------------------------------

    def log(self, message):

        self.log_window.append(message)