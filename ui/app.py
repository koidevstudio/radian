from __future__ import annotations
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QSplitter, QLabel,
)
from PySide6.QtCore import Qt
import sys
from ui.state import AppState
from ui.widgets.preview_canvas import PreviewCanvas
from ui.widgets.layer_list import LayerList
from ui.widgets.properties_panel import PropertiesPanel
from ui.panels.toolbar_panel import ToolbarPanel
from ui.constants import PANEL_WIDTH


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Radian - By Koi")

        self._state = AppState()
        self._state.set_on_change(self._on_change)

        # Toolbar
        toolbar = ToolbarPanel(self._state)
        self.addToolBar(Qt.TopToolBarArea, self._wrap_toolbar(toolbar))

        # Central
        central = QWidget()
        root    = QVBoxLayout(central)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(4)
        self.setCentralWidget(central)

        splitter = QSplitter(Qt.Horizontal)
        root.addWidget(splitter)

        # Left Panel
        left = QWidget()
        left.setMinimumWidth(PANEL_WIDTH)
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 8, 0)
        left_layout.setSpacing(20)

        self._layer_list = LayerList()
        self._layer_list.selection_changed.connect(self._on_select)
        self._layer_list.add_requested.connect(self._on_add)
        self._layer_list.delete_requested.connect(self._on_delete)
        self._layer_list.move_requested.connect(self._on_move)
        left_layout.addWidget(self._layer_list)

        self._props = PropertiesPanel()
        self._props.changed.connect(self._on_change)
        left_layout.addWidget(self._props)
        left_layout.addStretch(1)
        
        splitter.addWidget(left)

        # Right Panel
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(4)
        right_layout.addWidget(QLabel("Preview"))

        self._canvas = PreviewCanvas()
        right_layout.addWidget(self._canvas, stretch=1)

        splitter.addWidget(right)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        # Seed default element and load its properties
        self._state.add_marks()
        element = self._state.get_selected()
        if element:
            self._props.load(element)
        self._on_change()

    # Slots

    def _on_change(self) -> None:
        self._canvas.refresh(self._state.elements, self._state.render_config)
        self._layer_list.refresh(self._state.elements, self._state.selected_id)

    def _on_select(self, uid: str) -> None:
        self._state.selected_id = uid
        element = self._state.get_selected()
        if element:
            self._props.load(element)
        self._on_change()

    def _on_add(self, kind: str) -> None:
        {"marks": self._state.add_marks,
         "rings": self._state.add_rings,
         "typography": self._state.add_typography}[kind]()
        element = self._state.get_selected()
        if element:
            self._props.load(element)
        self._on_change()

    def _on_delete(self) -> None:
        self._state.delete_selected()
        element = self._state.get_selected()
        if element:
            self._props.load(element)
        else:
            self._props.clear()
        self._on_change()

    def _on_move(self, direction: str) -> None:
        {"up": self._state.move_up, "down": self._state.move_down}[direction]()
        self._on_change()

    @staticmethod
    def _wrap_toolbar(widget: QWidget):
        from PySide6.QtWidgets import QToolBar
        tb = QToolBar()
        tb.setMovable(False)
        tb.addWidget(widget)
        return tb


def run() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())