from PyQt5.QtWidgets import (
    QPushButton,
    QWidget,
    QFileDialog,
    QVBoxLayout,
    QLabel,
    QSpinBox,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt5.QtGui import QPixmap, QImage
from helpers.pdf import get_number_of_pages, pdf_to_image
from PyQt5.QtCore import Qt, QSize
from PIL.Image import Image


class PdfDisplayWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.file_path = None
        self.pdf_images: list[Image | None] = []

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: lightblue;")

        layout = QVBoxLayout(self)

        toolbar = self.construct_toolbar()
        layout.addLayout(toolbar)

        self.image_label = QLabel()
        layout.addWidget(self.image_label)

        self.set_image_label("Please open a PDF file to display its pages.")

    def construct_toolbar(self) -> QHBoxLayout:
        toolbar = QHBoxLayout(self)

        self.file_button = QPushButton("Open PDF")
        self.file_button.clicked.connect(self.upload_pdf)
        toolbar.addWidget(self.file_button, 2)

        self.page_selector = QSpinBox()
        self.page_selector.setValue(0)
        self.page_selector.setDisabled(True)
        self.page_selector.valueChanged.connect(self.display_page)
        toolbar.addWidget(self.page_selector, 1)

        self.number_of_pages_label = QLabel("of 0 pages")
        self.page_selector.valueChanged.connect(
            lambda _: self.number_of_pages_label.setText(
                f"of {self.page_selector.maximum()} pages"
            )
        )
        self.number_of_pages_label.setSizePolicy(
            QSizePolicy.Maximum, QSizePolicy.Maximum
        )
        toolbar.addWidget(self.number_of_pages_label, 1)

        return toolbar

    def upload_pdf(self):
        self.set_image_label("Loading PDF...")

        file_path = QFileDialog.getOpenFileName(
            self, "Open PDF file", ".", "PDF file (*.pdf)"
        )

        if not file_path[0]:
            return

        self.file_path = file_path[0]

        max_number_of_pages = get_number_of_pages(self.file_path)
        self.page_selector.setRange(1, max_number_of_pages)
        self.page_selector.setDisabled(False)
        self.page_selector.setValue(1)

        self.pdf_images = [None for _ in range(max_number_of_pages)]

        self.display_page(1)

    def get_image(self, page_number: int) -> Image | None:
        page_image = self.pdf_images[page_number - 1]
        if page_image is not None:
            return page_image

        if self.file_path is None:
            self.set_image_label("No PDF file loaded.")
            return

        page_image = pdf_to_image(self.file_path, page_number)
        self.pdf_images[page_number - 1] = page_image

        return page_image

    def display_page(self, page_number):
        try:
            image = self.get_image(page_number)

            if image is None:
                self.set_image_label("Error loading page")
                return

            qimage = QImage(
                image.tobytes(), image.width, image.height, QImage.Format_RGB888
            )

            pixmap = QPixmap.fromImage(qimage).scaled(
                QSize(self.image_label.width(), self.image_label.height()),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            self.set_image_label(pixmap)
        except:
            self.set_image_label("Error displaying page")

    def set_image_label(self, image_label):
        self.image_label.clear()

        if isinstance(image_label, QPixmap):
            pixmap = image_label
            message = ""
        else:
            pixmap = QPixmap()
            message = image_label

        self.image_label.setPixmap(pixmap)
        self.image_label.setText(message)
