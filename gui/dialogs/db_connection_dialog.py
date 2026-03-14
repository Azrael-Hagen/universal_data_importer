from gui.dialogs.db_connection_dialog import DBConnectionDialog
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox
)


class DBConnectionDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Database Connection")

        layout = QVBoxLayout()

        self.db_type = QComboBox()
        self.db_type.addItems(["sqlite", "mysql", "postgres"])

        self.host = QLineEdit()
        self.host.setPlaceholderText("Host")

        self.database = QLineEdit()
        self.database.setPlaceholderText("Database")

        self.user = QLineEdit()
        self.user.setPlaceholderText("User")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")

        self.connect_btn = QPushButton("Connect")

        layout.addWidget(QLabel("Database Type"))
        layout.addWidget(self.db_type)

        layout.addWidget(self.host)
        layout.addWidget(self.database)
        layout.addWidget(self.user)
        layout.addWidget(self.password)

        layout.addWidget(self.connect_btn)

        self.setLayout(layout)
