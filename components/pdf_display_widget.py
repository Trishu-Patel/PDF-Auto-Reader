from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt

class PdfDisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: lightblue;")
        
        left_layout = QVBoxLayout(self)
        left_label = QLabel("PDF Display")
        left_label.setAlignment(Qt.AlignCenter)
        left_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        left_layout.addWidget(left_label)