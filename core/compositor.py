from __future__ import annotations
import math
import skia
from core.models import (
    Element, Mask, RenderConfig,
    MarksElement, RingsElement, TypographyElement,
)
from elements.base import ElementRenderer, color_to_skia
from elements.marks import MarksRenderer
from elements.rings import RingsRenderer
from elements.typography import TypographyRenderer

# Maps each concrete type to its renderer

_REGISTRY: dict[type[Element], ElementRenderer] = {
    MarksElement:      MarksRenderer(),
    RingsElement:      RingsRenderer(),
    TypographyElement: TypographyRenderer(),
}

def _get_renderer(element: Element) -> ElementRenderer:
    renderer = _REGISTRY.get(type(element))
    if renderer is None:
        raise TypeError(f"No renderer registered for {type(element).__name__}")
    return renderer


# Mask

def _apply_mask(canvas: skia.Canvas, mask: Mask, center: float, size: float) -> None:
    """
    Cuts a sector out of the element surface using DstOut blend.
    The sector is defined by mask.angle (aperture) and mask.rotation (orientation).
    """
    rot   = math.radians(mask.rotation) - math.pi / 2
    half  = math.radians(mask.angle) / 2
    a_l   = rot - half
    a_r   = rot + half

    max_r = math.sqrt(2) * size * 2          # guaranteed to reach every corner
    steps = max(50, int(mask.angle))

    path = skia.Path()
    path.moveTo(center, center)
    path.lineTo(
        center + max_r * math.cos(a_l),
        center + max_r * math.sin(a_l),
    )
    for i in range(1, steps + 1):
        t = i / steps
        a = a_l + (a_r - a_l) * t
        path.lineTo(center + max_r * math.cos(a), center + max_r * math.sin(a))
    path.close()

    paint = skia.Paint()
    paint.setStyle(skia.Paint.kFill_Style)
    paint.setAntiAlias(True)
    paint.setColor(skia.ColorWHITE)
    paint.setBlendMode(skia.BlendMode.kDstOut)
    canvas.drawPath(path, paint)


# Surface helpers

def _make_transparent_surface(size: int) -> skia.Surface:
    surface = skia.Surface(size, size)
    surface.getCanvas().clear(skia.ColorTRANSPARENT)
    return surface

def _make_background_surface(config: RenderConfig) -> skia.Surface:
    surface = skia.Surface(config.canvas_size, config.canvas_size)
    canvas  = surface.getCanvas()
    if config.transparent:
        canvas.clear(skia.ColorTRANSPARENT)
    else:
        canvas.clear(color_to_skia(config.bg_color))
    return surface


# Per-element compositing

def _render_element_to_surface(
    element: Element,
    config: RenderConfig,
    scale: float = 1.0
) -> skia.Surface:
    """
    Renders one element plus an optional mask onto its own transparent surface.
    Returns the surface; caller composites onto the canvas.
    """
    size    = config.canvas_size
    center  = size / 2.0
    surface = _make_transparent_surface(size)
    canvas  = surface.getCanvas()

    if scale != 1.0:
        canvas.scale(scale, scale)

    renderer = _get_renderer(element)
    renderer.draw(canvas, element, center / scale if scale != 0 else center)

    if element.mask.enabled:
        _apply_mask(canvas, element.mask, center / scale, size / scale)

    return surface


# Public API

def composite(elements: list[Element], config: RenderConfig,scale: float = 1.0) -> skia.Surface:
    """
    Composites all visible elements sorted by z_index onto a single surface.

    Each element:
    1. Renders into its own transparent surface.
    2. Is stamped onto the canvas (master) with kSrcOver.

    Returns the final composited surface.
    """
    master  = _make_background_surface(config)
    canvas  = master.getCanvas()

    ordered = sorted(
        (el for el in elements if el.visible),
        key=lambda el: el.z_index,
    )

    for element in ordered:
        elem_surface = _render_element_to_surface(element, config, scale)
        image        = elem_surface.makeImageSnapshot()
        canvas.drawImage(image, 0, 0)

    return master