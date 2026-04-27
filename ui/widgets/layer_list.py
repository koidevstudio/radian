from __future__ import annotations
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton, QLabel,
)
from PySide6.QtCore import Signal
from core.models import Element


class LayerList(QWidget):

    selection_changed = Signal(str)
    add_requested     = Signal(str)
    delete_requested  = Signal()
    move_requested    = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._building = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)             

        lbl = QLabel("<h2><b>Layers</b></h2>")
        layout.addWidget(lbl)

        self._list = QListWidget()
        self._list.setMaximumHeight(200)    
        self._list.setSpacing(1)
        self._list.currentItemChanged.connect(self._on_item_changed)
        layout.addWidget(self._list)

        add_row = QHBoxLayout()
        add_row.setSpacing(4)
        for label, kind in [("+ Marks", "marks"), ("+ Ring", "rings"), ("+ Text", "typography")]:
            btn = QPushButton(label)
            btn.setFixedHeight(24)
            btn.clicked.connect(lambda _=False, k=kind: self.add_requested.emit(k))
            add_row.addWidget(btn)
        layout.addLayout(add_row)

        action_row = QHBoxLayout()
        action_row.setSpacing(4)
        for label, action in [("Move Up", "up"), ("Move Down", "down")]:
            btn = QPushButton(label)
            btn.setFixedHeight(24)
            btn.clicked.connect(lambda _=False, a=action: self.move_requested.emit(a))
            action_row.addWidget(btn)
        del_btn = QPushButton("Delete")
        del_btn.setFixedHeight(24)
        del_btn.clicked.connect(self.delete_requested.emit)
        action_row.addWidget(del_btn)
        layout.addLayout(action_row)

    def refresh(self, elements: list[Element], selected_id: str | None) -> None:
        self._building = True
        self._list.clear()
        for el in reversed(elements):
            item = QListWidgetItem(el.label)
            item.setData(256, el.id)
            self._list.addItem(item)
            if el.id == selected_id:
                self._list.setCurrentItem(item)
        self._building = False

    def _on_item_changed(self, current: QListWidgetItem, _) -> None:
        if self._building or current is None:
            return
        self.selection_changed.emit(current.data(256))