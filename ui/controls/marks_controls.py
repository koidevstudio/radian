from __future__ import annotations
from PySide6.QtWidgets import QFormLayout, QRadioButton, QHBoxLayout, QWidget, QLabel
from core.models import MarksElement, MarkType
from ui.controls.base_controls import BaseControls


class MarksControls(BaseControls):

    def __init__(self, element: MarksElement, parent=None) -> None:
        super().__init__(parent)
        self._el = element
        form = QFormLayout(self)
        form.setSpacing(8)
        form.setContentsMargins(0, 0, 0, 0)

        form.addRow(QLabel("<b>Marks</b>"))

        count_row, _ = self._slider_int(element.count, 1, 360)
        count_row.slider.valueChanged.connect(lambda v: self._set("count", v))
        form.addRow("Count", count_row)

        radius_row, _ = self._slider_int(element.radius, 10, 960)
        radius_row.slider.valueChanged.connect(
            lambda v: self._set("radius", v)
        )
        form.addRow("Radius", radius_row)

        length_row, _ = self._slider_int(element.length, 1, 400)
        length_row.slider.valueChanged.connect(
            lambda v: self._set("length", v)
        )
        form.addRow("Length", length_row)

        width_row, _ = self._slider_int(element.width, 1, 400)
        width_row.slider.valueChanged.connect(
            lambda v: self._set("width", v)
        )
        form.addRow("Width", width_row)

        type_row = QWidget()
        type_layout = QHBoxLayout(type_row)
        type_layout.setContentsMargins(0, 0, 0, 0)
        self._rb_line   = QRadioButton("Line")
        self._rb_circle = QRadioButton("Circle")
        (self._rb_line if element.mark_type == MarkType.LINE else self._rb_circle).setChecked(True)
        self._rb_line.toggled.connect(self._on_type_toggle)
        type_layout.addWidget(self._rb_line)
        type_layout.addWidget(self._rb_circle)
        form.addRow("Type", type_row)

        color_btn = self._color_btn(element.color, lambda c: self._set("color", c))
        form.addRow("Color", color_btn)

    def _set(self, attr: str, val) -> None:
        setattr(self._el, attr, val)
        self.changed.emit()

    def _on_type_toggle(self) -> None:
        self._el.mark_type = MarkType.LINE if self._rb_line.isChecked() else MarkType.CIRCLE
        self.changed.emit()