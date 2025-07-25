import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout

from components.pdf_display_widget import PdfDisplayWidget
from components.text_player_widget import TextPlayerWidget
from helpers.ocr import optical_character_recognition
from PIL.Image import Image


class PdfAutoReaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PDF Auto Reader")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.pdf_display_widget = PdfDisplayWidget()
        self.text_player_widget = TextPlayerWidget()

        self.pdf_display_widget.set_process_snippet_callback(self.process_snippet)

        self.main_layout.addWidget(self.pdf_display_widget, 4)
        self.main_layout.addWidget(self.text_player_widget, 5)

        self.showMaximized()

    def process_snippet(self, image: Image):
        text = optical_character_recognition(image)

        self.text_player_widget.set_text(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PdfAutoReaderApp()
    window.show()
    sys.exit(app.exec_())
