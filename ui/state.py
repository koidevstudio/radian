from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from typing import Callable
from core.models import (
    Color, Mask, RenderConfig,
    MarksElement, RingsElement, TypographyElement, Element,
)


def _new_id() -> str:
    return str(uuid.uuid4())[:8]


@dataclass
class AppState:
    elements:      list[Element] = field(default_factory=list)
    selected_id:   str | None    = None
    render_config: RenderConfig  = field(default_factory=RenderConfig)
    _on_change:    Callable      = field(default=lambda: None, repr=False)

    def set_on_change(self, cb: Callable) -> None:
        self._on_change = cb

    def notify(self) -> None:
        self._on_change()

    def add_marks(self) -> MarksElement:
        el = MarksElement(
            id=_new_id(),
            label=f"Marks {len(self.elements) + 1}",
            z_index=len(self.elements),
        )
        self.elements.append(el)
        self.selected_id = el.id
        return el

    def add_rings(self) -> RingsElement:
        el = RingsElement(
            id=_new_id(),
            label=f"Ring {len(self.elements) + 1}",
            z_index=len(self.elements),
        )
        self.elements.append(el)
        self.selected_id = el.id
        return el

    def add_typography(self) -> TypographyElement:
        el = TypographyElement(
            id=_new_id(),
            label=f"Text {len(self.elements) + 1}",
            text="SAMPLE TEXT",
            z_index=len(self.elements),
        )
        self.elements.append(el)
        self.selected_id = el.id
        return el

    def delete_selected(self) -> None:
        if self.selected_id is None:
            return
        self.elements = [e for e in self.elements if e.id != self.selected_id]
        self.selected_id = self.elements[-1].id if self.elements else None

    def move_up(self) -> None:
        idx = self._selected_index()
        if idx is None or idx >= len(self.elements) - 1:
            return
        self.elements[idx], self.elements[idx + 1] = (
            self.elements[idx + 1], self.elements[idx]
        )
        self._reindex()

    def move_down(self) -> None:
        idx = self._selected_index()
        if idx is None or idx == 0:
            return
        self.elements[idx], self.elements[idx - 1] = (
            self.elements[idx - 1], self.elements[idx]
        )
        self._reindex()

    def get_selected(self) -> Element | None:
        if self.selected_id is None:
            return None
        return next((e for e in self.elements if e.id == self.selected_id), None)

    def _selected_index(self) -> int | None:
        for i, e in enumerate(self.elements):
            if e.id == self.selected_id:
                return i
        return None

    def _reindex(self) -> None:
        for i, e in enumerate(self.elements):
            e.z_index = i