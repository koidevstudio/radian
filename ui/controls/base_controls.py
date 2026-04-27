from __future__ import annotations
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QSlider, QLabel, QPushButton,QSpinBox
)
from PySide6.QtCore import Signal, Qt


class BaseControls(QWidget):

    changed = Signal()

    
    # Slider row
    
    def _slider_int(
        self,
        value: int,
        min_val: int,
        max_val: int,
        step: int = 1,
    ) -> tuple[QWidget, "callable"]:
        row    = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(value)
        slider.setSingleStep(step)

        spin = QSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(int(value))
        spin.setFixedWidth(50)

        slider.valueChanged.connect(spin.setValue)
        spin.valueChanged.connect(slider.setValue)
        
        layout.addWidget(slider)
        layout.addWidget(spin)

        row.slider = slider

        def setter(v: int):
            slider.blockSignals(True)
            slider.setValue(v)
            spin.setValue(v)
            slider.blockSignals(False)

        return row, setter

    def _color_btn(self, color, callback) -> QPushButton:
        from PySide6.QtGui import QColor
        btn = QPushButton()
        btn.setFixedSize(48, 24)
        self._apply_btn_color(btn, color)

        def pick():
            from PySide6.QtWidgets import QColorDialog
            from core.models import Color
            qc = QColorDialog.getColor(
                QColor(int(color.r * 255), int(color.g * 255), int(color.b * 255)),
                self,
            )
            if qc.isValid():
                new_color = Color(qc.redF(), qc.greenF(), qc.blueF())
                self._apply_btn_color(btn, new_color)
                callback(new_color)

        btn.clicked.connect(pick)
        return btn

    @staticmethod
    def _apply_btn_color(btn: QPushButton, color) -> None:
        r = int(color.r * 255)
        g = int(color.g * 255)
        b = int(color.b * 255)
        btn.setStyleSheet(
            f"background-color: rgb({r},{g},{b}); border: 1px solid #666;"
        )