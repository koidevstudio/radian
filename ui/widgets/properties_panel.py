from __future__ import annotations
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel, QSizePolicy,
)
from PySide6.QtCore import Signal
from core.models import Element, MarksElement, RingsElement, TypographyElement
from ui.controls.marks_controls import MarksControls
from ui.controls.rings_controls import RingsControls
from ui.controls.typography_controls import TypographyControls
from ui.controls.mask_controls import MaskControls


class PropertiesPanel(QWidget):
    changed = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLabel("<span style='font-size: 16px; font-weight: bold;'>Properties</span>"))
        
        self.setMinimumHeight(600)
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self._scroll)

        self._show_empty()

    def load(self, element: Element) -> None:
        container = QWidget()
        layout    = QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        if isinstance(element, MarksElement):
            ctrl = MarksControls(element)
            ctrl.changed.connect(self.changed)
            layout.addWidget(ctrl)

        elif isinstance(element, RingsElement):
            ctrl = RingsControls(element)
            ctrl.changed.connect(self.changed)
            layout.addWidget(ctrl)

        elif isinstance(element, TypographyElement):
            ctrl = TypographyControls(element)
            ctrl.changed.connect(self.changed)
            layout.addWidget(ctrl)

        mask_ctrl = MaskControls(element)
        mask_ctrl.changed.connect(self.changed)
        layout.addWidget(mask_ctrl)

        layout.addStretch()
        self._scroll.setWidget(container)

    def clear(self) -> None:
        self._show_empty()

    def _show_empty(self) -> None:
        w = QWidget()
        QVBoxLayout(w).addWidget(QLabel("No element selected"))
        self._scroll.setWidget(w)