from __future__ import annotations
from PySide6.QtWidgets import QFormLayout, QLabel
from core.models import RingsElement
from ui.controls.base_controls import BaseControls


class RingsControls(BaseControls):

    def __init__(self, element: RingsElement, parent=None) -> None:
        super().__init__(parent)
        self._el = element
        form = QFormLayout(self)
        form.setSpacing(8)
        form.setContentsMargins(0, 0, 0, 0)

        form.addRow(QLabel("<b>Ring</b>"))

        radius_row, _ = self._slider_int(element.radius, 10, 960)
        radius_row.slider.valueChanged.connect(
            lambda v: self._set("radius", v)
        )
        form.addRow("Radius", radius_row)

        thickness_row, _ = self._slider_int(element.thickness, 1, 400)
        thickness_row.slider.valueChanged.connect(
            lambda v: self._set("thickness", v)
        )
        form.addRow("Thickness", thickness_row)

        color_btn = self._color_btn(element.color, lambda c: self._set("color", c))
        form.addRow("Color", color_btn)

    def _set(self, attr: str, val) -> None:
        setattr(self._el, attr, val)
        self.changed.emit()