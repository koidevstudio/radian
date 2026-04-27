from __future__ import annotations
import numpy as np
from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt
from core.models import Element, RenderConfig
from core.renderer import Renderer


class PreviewCanvas(QLabel):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(300, 300)
        self.setStyleSheet("background-color: #1e1e1e;")
        self._elements: list[Element] = []
        self._config: RenderConfig | None = None

    def refresh(self, elements: list[Element], config: RenderConfig) -> None:
        self._elements = elements
        self._config   = config
        self._redraw()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._redraw()

    def _redraw(self) -> None:
        if self._config is None:
            return

        # Use the smaller of width/height to keep it square
        size = min(self.width(), self.height())
        if size < 10:
            return

        renderer = Renderer(self._config)
        surface  = renderer.render_preview(self._elements, size)
        image    = surface.makeImageSnapshot()

        arr = np.frombuffer(image.tobytes(), dtype=np.uint8).reshape(size, size, 4)
        arr = arr[:, :, [2, 1, 0, 3]].copy()

        qimg = QImage(arr.data, size, size, size * 4, QImage.Format_RGBA8888)
        self.setPixmap(QPixmap.fromImage(qimg))