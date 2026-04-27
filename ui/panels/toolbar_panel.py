from __future__ import annotations
from pathlib import Path
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel,
    QPushButton, QCheckBox, QMessageBox,
)
from PySide6.QtGui import QColor
from ui.state import AppState
from export.exporter import Exporter, ExportConfig


class ToolbarPanel(QWidget):

    def __init__(self, state: AppState, parent=None) -> None:
        super().__init__(parent)
        self._state = state
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(12)

        layout.addWidget(QLabel("Background:"))

        self._bg_btn = QPushButton()
        self._bg_btn.setFixedSize(48, 24)
        self._set_bg_btn_color(QColor(255, 255, 255))
        self._bg_btn.clicked.connect(self._pick_bg)
        layout.addWidget(self._bg_btn)

        transparent_cb = QCheckBox("Transparent")
        transparent_cb.toggled.connect(self._on_transparent_toggled)
        layout.addWidget(transparent_cb)

        layout.addStretch()

        export_btn = QPushButton("Export PNG")
        export_btn.clicked.connect(self._export)
        layout.addWidget(export_btn)

    def _pick_bg(self) -> None:
        from PySide6.QtWidgets import QColorDialog
        from core.models import Color
        qc = QColorDialog.getColor(parent=self)
        if qc.isValid():
            self._set_bg_btn_color(qc)
            self._state.render_config.bg_color = Color(qc.redF(), qc.greenF(), qc.blueF())
            self._state.notify()

    def _on_transparent_toggled(self, checked: bool) -> None:
        self._state.render_config.transparent = checked
        self._state.notify()

    def _set_bg_btn_color(self, qc: QColor) -> None:
        self._bg_btn.setStyleSheet(
            f"background-color: {qc.name()}; border: 1px solid #555;"
        )

    def _export(self) -> None:
        
        
        # Name based on timestamp to ensure uniqueness and avoid overwriting previous exports
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_{timestamp}.png"
        
        # Make sure the output directory exists
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        ec = ExportConfig(
            output_path=output_dir / filename,
            canvas_size=self._state.render_config.canvas_size,
            dpi=self._state.render_config.dpi,
            transparent=self._state.render_config.transparent,
        )
        try:
            result = Exporter(ec).export_png_with_metadata(
                self._state.elements, self._state.render_config
            )
            msg = (
                f"Saved to:\n{result['path']}\n\n"
                f"{result['canvas_size']}×{result['canvas_size']}px  "
                f"· {result['dpi']} DPI  "
                f"· {result['num_layers']} layers"
            )
            QMessageBox.information(self, "Export complete", msg)
        except Exception as e:
            QMessageBox.critical(self, "Export failed", str(e))