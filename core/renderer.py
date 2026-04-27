from __future__ import annotations
import skia
from core.models import Element, RenderConfig
from core.compositor import composite


class Renderer:
    """
    This is the only class the UI and exporter need to import.

    Responsibilities:
      - Accept a RenderConfig and element list
      - Delegate to compositor
      - Return a skia.Surface
    """

    def __init__(self, config: RenderConfig) -> None:
        self.config = config

    def render(self, elements: list[Element]) -> skia.Surface:
        """Composite all elements and return the final surface"""
        return composite(elements, self.config)

    def render_preview(
        self,
        elements: list[Element],
        preview_size: int = 512,
    ) -> skia.Surface:
        
        original_size = self.config.canvas_size
        scale_factor = preview_size / original_size
        
        preview_config = RenderConfig(
            canvas_size=preview_size,
            dpi=72,
            bg_color=self.config.bg_color,
            transparent=self.config.transparent,
        )
        return composite(elements, preview_config, scale=scale_factor)