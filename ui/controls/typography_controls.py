from __future__ import annotations
from PySide6.QtWidgets import (
    QFormLayout, QLabel, QLineEdit, QCheckBox, QComboBox,
)
from core.models import TypographyElement
from fonts.font_manager import list_available_fonts, list_variants
from ui.controls.base_controls import BaseControls


class TypographyControls(BaseControls):

    def __init__(self, element: TypographyElement, parent=None) -> None:
        super().__init__(parent)
        self._el = element
        form = QFormLayout(self)
        form.setSpacing(8)
        form.setContentsMargins(0, 0, 0, 0)

        form.addRow(QLabel("<b>Typography</b>"))

        text = QLineEdit(element.text)
        text.textChanged.connect(lambda v: self._set("text", v))
        form.addRow("Text", text)

        radius_row, _ = self._slider_int(element.radius, 10, 960)
        radius_row.slider.valueChanged.connect(
            lambda v: self._set("radius", v)
        )
        form.addRow("Radius", radius_row)

        size_row, _ = self._slider_int(element.font_size, 6, 200)
        size_row.slider.valueChanged.connect(
            lambda v: self._set("font_size", v)
        )
        form.addRow("Font size", size_row)

        spacing_row, _ = self._slider_int(element.letter_spacing, -20, 80)
        spacing_row.slider.valueChanged.connect(
            lambda v: self._set("letter_spacing", v)
        )
        form.addRow("Spacing", spacing_row)

        rotation_row, _ = self._slider_int(element.rotation, -180, 180)
        rotation_row.slider.valueChanged.connect(
            lambda v: self._set("rotation", v)
        )
        form.addRow("Rotation", rotation_row)

        flip = QCheckBox("Flip 180°")
        flip.setChecked(element.flip)
        flip.toggled.connect(lambda v: self._set("flip", v))
        form.addRow("", flip)

        self._family_combo = QComboBox()
        fonts = list_available_fonts()
        self._family_combo.addItems(fonts)
        if element.font_family in fonts:
            self._family_combo.setCurrentText(element.font_family)
        self._family_combo.currentTextChanged.connect(self._on_family_changed)
        form.addRow("Font", self._family_combo)

        self._variant_combo = QComboBox()
        self._populate_variants(element.font_family)
        self._variant_combo.currentTextChanged.connect(lambda v: self._set("font_variant", v))
        form.addRow("Variant", self._variant_combo)

        color_btn = self._color_btn(element.color, lambda c: self._set("color", c))
        form.addRow("Color", color_btn)

    def _set(self, attr: str, val) -> None:
        setattr(self._el, attr, val)
        self.changed.emit()

    def _on_family_changed(self, family: str) -> None:
        self._el.font_family = family
        self._populate_variants(family)
        self.changed.emit()

    def _populate_variants(self, family: str) -> None:
        variants = list_variants(family) or ["Regular"]
        self._variant_combo.blockSignals(True)
        self._variant_combo.clear()
        self._variant_combo.addItems(variants)
        current = self._el.font_variant
        self._variant_combo.setCurrentText(current if current in variants else variants[0])
        self._variant_combo.blockSignals(False)