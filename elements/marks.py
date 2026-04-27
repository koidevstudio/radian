from __future__ import annotations
import math
import skia
from core.models import MarksElement, MarkType
from elements.base import ElementRenderer, make_paint


class MarksRenderer(ElementRenderer):

    def draw(self, canvas: skia.Canvas, element: MarksElement, center: float) -> None:
        if element.mark_type == MarkType.LINE:
            self._draw_lines(canvas, element, center)
        else:
            self._draw_circles(canvas, element, center)

    def _draw_lines(
        self, canvas: skia.Canvas, element: MarksElement, center: float
    ) -> None:
        paint = make_paint(
            element.color,
            style=skia.Paint.kStroke_Style,
            stroke_width=element.width,
        )
        step = 360.0 / element.count
        for i in range(element.count):
            angle = math.radians(i * step - 90)
            cos_a, sin_a = math.cos(angle), math.sin(angle)
            inner = element.radius - element.length
            canvas.drawLine(
                center + inner * cos_a,
                center + inner * sin_a,
                center + element.radius * cos_a,
                center + element.radius * sin_a,
                paint,
            )

    def _draw_circles(
        self, canvas: skia.Canvas, element: MarksElement, center: float
    ) -> None:
        paint = make_paint(element.color, style=skia.Paint.kFill_Style)
        dot_radius = max(element.width, 2.0)
        step = 360.0 / element.count
        for i in range(element.count):
            angle = math.radians(i * step - 90)
            canvas.drawCircle(
                center + element.radius * math.cos(angle),
                center + element.radius * math.sin(angle),
                dot_radius,
                paint,
            )