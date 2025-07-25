from PyQt5.QtWidgets import (
    QPushButton,
    QWidget,
    QFileDialog,
    QVBoxLayout,
    QLabel,
    QSpinBox,
    QHBoxLayout,
    QSizePolicy,
    QGraphicsScene,
)
from PyQt5.QtGui import QPixmap, QImage
from components.pdf_snippet_tool import PdfSnippetTool
from helpers.image_processing import process_image
from helpers.pdf import get_number_of_pages, pdf_to_image
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

        self.graphics_scene = QGraphicsScene()
        self.graphics_view = PdfSnippetTool(self.graphics_scene)

        layout.addWidget(self.graphics_view)

        self.set_image_label("Please open a PDF file to display its pages.")

    def construct_toolbar(self) -> QHBoxLayout:
        toolbar = QHBoxLayout(self)

        self.file_button = QPushButton("Open PDF")
        self.file_button.clicked.connect(self.upload_pdf)
        toolbar.addWidget(self.file_button, 4)

        self.zoom_out_button = QPushButton("-")
        self.zoom_out_button.clicked.connect(self.zoom_out)
        toolbar.addWidget(self.zoom_out_button, 1)

        self.zoom_in_button = QPushButton("+")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        toolbar.addWidget(self.zoom_in_button, 1)

        self.page_selector = QSpinBox()
        self.page_selector.setValue(0)
        self.page_selector.setDisabled(True)
        self.page_selector.valueChanged.connect(self.display_page)
        toolbar.addWidget(self.page_selector, 2)

        self.number_of_pages_label = QLabel("of 0 pages")
        self.page_selector.valueChanged.connect(
            lambda _: self.number_of_pages_label.setText(
                f"of {self.page_selector.maximum()} pages"
            )
        )
        self.number_of_pages_label.setSizePolicy(
            QSizePolicy.Maximum, QSizePolicy.Maximum
        )
        toolbar.addWidget(self.number_of_pages_label, 2)

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

            pixmap = QPixmap.fromImage(qimage)
            self.set_image_label(pixmap)
        except:
            self.set_image_label("Error displaying page")

    def set_image_label(self, image_label):
        self.graphics_scene.clear()

        if isinstance(image_label, QPixmap):
            self.graphics_scene.addPixmap(image_label)
        else:
            self.graphics_scene.addText(str(image_label))

    def zoom_in(self):
        self.graphics_view.zoom_in()

    def zoom_out(self):
        self.graphics_view.zoom_out()

    def get_current_page(self) -> Image | None:
        return self.get_image(self.page_selector.value())

    def set_process_snippet_callback(self, callback):

        def new_callback(x1: int, y1: int, x2: int, y2: int):
            image = self.get_current_page()
            if image is None:
                return
            image = process_image(image, x1, y1, x2, y2)
            callback(image)

        self.graphics_view.set_process_snippet_callback(new_callback)
