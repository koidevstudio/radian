from __future__ import annotations
from PySide6.QtWidgets import QFormLayout, QLabel, QCheckBox
from core.models import Element, Mask
from ui.controls.base_controls import BaseControls


class MaskControls(BaseControls):

    def __init__(self, element: Element, parent=None) -> None:
        super().__init__(parent)
        self._el = element
        form = QFormLayout(self)
        form.setSpacing(8)
        form.setContentsMargins(0, 0, 0, 0)

        form.addRow(QLabel("<b>Mask</b>"))

        enabled = QCheckBox("Enable")
        enabled.setChecked(element.mask.enabled)
        enabled.toggled.connect(lambda v: self._update(enabled=v))
        form.addRow("", enabled)

        angle_row, _ = self._slider_int(element.mask.angle, 1, 360)
        angle_row.slider.valueChanged.connect(
            lambda v: self._update(angle=v)
        )
        form.addRow("Angle", angle_row)

        rotation_row, _ = self._slider_int(element.mask.rotation, 0, 360)
        rotation_row.slider.valueChanged.connect(
            lambda v: self._update(rotation=v)
        )
        form.addRow("Rotation", rotation_row)

    def _update(self, **kwargs) -> None:
        m = self._el.mask
        self._el.mask = Mask(
            enabled=kwargs.get("enabled",  m.enabled),
            angle=kwargs.get("angle",      m.angle),
            rotation=kwargs.get("rotation", m.rotation),
        )
        self.changed.emit()