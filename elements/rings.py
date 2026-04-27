from __future__ import annotations
import skia
from core.models import RingsElement
from elements.base import ElementRenderer, make_paint


class RingsRenderer(ElementRenderer):

    def draw(self, canvas: skia.Canvas, element: RingsElement, center: float) -> None:
        inner = element.radius - element.thickness

        # 1. Circle drawing
        canvas.drawCircle(
            center, center, element.radius,
            make_paint(element.color, style=skia.Paint.kFill_Style),
        )

        # 2. Punch out inner circle using DstOut blend, this leaves a transparent hole.
        punch = skia.Paint()
        punch.setColor(skia.ColorWHITE)
        punch.setStyle(skia.Paint.kFill_Style)
        punch.setAntiAlias(True)
        punch.setBlendMode(skia.BlendMode.kDstOut)
        canvas.drawCircle(center, center, inner, punch)