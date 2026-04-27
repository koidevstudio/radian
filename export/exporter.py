from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import skia
from core.models import Element, RenderConfig
from core.renderer import Renderer



# Export configuration

@dataclass
class ExportConfig:
    output_path:   Path
    canvas_size:   int  = 1920
    dpi:           int  = 300
    transparent:   bool = False


# Exporter

class Exporter:
    """
    Handles all export logic.
    Decoupled from Renderer so export settings can differ from preview settings
    """

    def __init__(self, export_config: ExportConfig) -> None:
        self.export_config = export_config

    def export_png(
        self,
        elements: list[Element],
        render_config: RenderConfig,
    ) -> Path:
        """
        Render at full export resolution and save to PNG.

        Args:
            elements:      The full layer stack.
            render_config: Config used for bg_color / transparent flag.

        Returns:
            Path to the written PNG file.
        """
        ec = self.export_config

        # Build an export-specific RenderConfig that overrides canvas size/dpi
        # but inherits visual settings (bg_color, transparent) from the UI config.
        export_render_config = RenderConfig(
            canvas_size=ec.canvas_size,
            dpi=ec.dpi,
            bg_color=render_config.bg_color,
            transparent=ec.transparent,
        )

        renderer = Renderer(export_render_config)
        surface  = renderer.render(elements)
        image    = surface.makeImageSnapshot()

        ec.output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(str(ec.output_path))

        return ec.output_path

    def export_png_with_metadata(
        self,
        elements: list[Element],
        render_config: RenderConfig,
    ) -> dict:
        """
        Export PNG and return a metadata dict for the UI to display.
        """
        path = self.export_png(elements, render_config)
        ec   = self.export_config
        return {
            "path":        str(path),
            "canvas_size": ec.canvas_size,
            "dpi":         ec.dpi,
            "transparent": ec.transparent,
            "num_layers":  len(elements),
        }