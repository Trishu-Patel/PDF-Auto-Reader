from PyQt5.QtWidgets import (
    QGraphicsView,
)
from PyQt5.QtGui import QMouseEvent, QPen, QPainter

from PyQt5.QtCore import Qt
from collections.abc import Callable

from utils.constants import ZOOM_STEP


class PdfSnippetTool(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setInteractive(True)

        self.dragging = False
        self.drag_start_pos = None
        self.drag_end_pos = None
        self.dash_rect_item = None

        self.process_image_callback: Callable[[int, int, int, int], None] | None = None

    def mousePressEvent(self, event: QMouseEvent | None):
        if event is None:
            return

        elif event.button() == Qt.MouseButton.RightButton:
            self.dragging = True
            self.drag_start_pos = self.mapToScene(event.pos())

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent | None):
        if event is None:
            return

        if event.button() == Qt.MouseButton.RightButton:

            if (
                self.process_image_callback is not None
                and self.drag_start_pos is not None
                and self.drag_end_pos is not None
            ):
                self.process_image_callback(
                    round(self.drag_start_pos.x()),
                    round(self.drag_start_pos.y()),
                    round(self.drag_end_pos.x()),
                    round(self.drag_end_pos.y()),
                )

            self.removeRectangle()
            self.dragging = False
            self.dash_rect_item = None
            self.drag_start_pos = None

        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent | None):
        if event is None:
            return

        if event.buttons() == Qt.MouseButton.RightButton:

            self.drag_end_pos = self.mapToScene(event.pos())

            self.removeRectangle()
            self.drawRectangle()

        super().mouseMoveEvent(event)

    def removeRectangle(self):
        if self.dash_rect_item:
            scene = self.scene()
            if scene is not None:
                scene.removeItem(self.dash_rect_item)

    def drawRectangle(self):
        if self.drag_start_pos is None or self.drag_end_pos is None:
            return

        rect = (
            min(self.drag_start_pos.x(), self.drag_end_pos.x()),
            min(self.drag_start_pos.y(), self.drag_end_pos.y()),
            abs(self.drag_start_pos.x() - self.drag_end_pos.x()),
            abs(self.drag_start_pos.y() - self.drag_end_pos.y()),
        )

        pen = QPen(Qt.GlobalColor.black)
        pen.setStyle(Qt.PenStyle.DashLine)
        pen.setWidth(2)
        scene = self.scene()
        if scene is not None:
            self.dash_rect_item = scene.addRect(*rect, pen)

    def zoom_in(self):
        self.scale(ZOOM_STEP, ZOOM_STEP)

    def zoom_out(self):
        self.scale(1 / ZOOM_STEP, 1 / ZOOM_STEP)

    def set_process_snippet_callback(
        self, callback: Callable[[int, int, int, int], None]
    ):
        self.process_image_callback = callback
