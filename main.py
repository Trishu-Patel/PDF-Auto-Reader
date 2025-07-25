import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout

from components.pdf_display_widget import PdfDisplayWidget
from components.text_player_widget import TextPlayerWidget

class PdfAutoReaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PDF Auto Reader")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        left_widget = PdfDisplayWidget()
        right_widget = TextPlayerWidget()
        
        main_layout.addWidget(left_widget, 4) 
        main_layout.addWidget(right_widget, 5) 
        
        self.showMaximized()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PdfAutoReaderApp()
    window.show()
    sys.exit(app.exec_())