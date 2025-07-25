from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt


class TextPlayerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: lightGreen;")

        left_layout = QVBoxLayout(self)
        self.label = QLabel("Text Player")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        left_layout.addWidget(self.label)

    def set_text(self, text: str):
        self.label.setText(text)
        self.label.adjustSize()
        self.label.setWordWrap(True)