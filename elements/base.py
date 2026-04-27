from __future__ import annotations
import abc
import skia
from core.models import Element, Color


def color_to_skia(color: Color) -> int:
    return skia.ColorSetRGB(
        int(color.r * 255),
        int(color.g * 255),
        int(color.b * 255),
    )

def make_paint(
    color: Color,
    style: skia.Paint.Style = skia.Paint.kFill_Style,
    stroke_width: float = 1.0,
    stroke_cap: skia.Paint.Cap = skia.Paint.kButt_Cap,
) -> skia.Paint:
    paint = skia.Paint()
    paint.setColor(color_to_skia(color))
    paint.setAntiAlias(True)
    paint.setStyle(style)
    paint.setStrokeWidth(stroke_width)
    paint.setStrokeCap(stroke_cap)
    return paint

class ElementRenderer(abc.ABC):
    """
    Stateless strategy — one subclass per RenderMode
    Receives a typed Element and draws onto the provided canvas
    Dont own a surface, the Compositor manages them.
    """

    @abc.abstractmethod
    def draw(self, canvas: skia.Canvas, element: Element, center: float) -> None:
        """Draw `element` onto `canvas`. `center` = canvas_size / 2."""