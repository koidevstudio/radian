from __future__ import annotations
import math
import skia
from core.models import TypographyElement
from elements.base import ElementRenderer, make_paint
from fonts.font_manager import get_font


class TypographyRenderer(ElementRenderer):

    def draw(
        self, canvas: skia.Canvas, element: TypographyElement, center: float
    ) -> None:
        if not element.text:
            return

        typeface = get_font(element.font_family, element.font_size, element.font_variant)
        if not typeface:
            return

        font   = skia.Font(typeface, element.font_size)
        paint  = make_paint(element.color, style=skia.Paint.kFill_Style)
        words  = [w for w in element.text.split(" ") if w]
        if not words:
            return

        if element.flip:
            words = words[::-1]

        metrics      = font.getMetrics()
        fallback_cy  = (metrics.fAscent + metrics.fDescent) / 2
        flip_offset  = 180.0 if element.flip else 0.0
        num_words    = len(words)

        for i, word in enumerate(words):
            base_angle  = math.radians(i * (360.0 / num_words) - 90)
            word_width  = self._word_width(font, word, element.letter_spacing)
            arc_span    = word_width / element.radius if element.radius > 0 else 0.0
            start_angle = base_angle - arc_span / 2

            cumulative = 0.0
            for char in word:
                char_w     = font.measureText(char)
                arc_offset = (cumulative + char_w / 2) / element.radius if element.radius > 0 else 0.0
                char_angle = start_angle + arc_offset

                cx = center + element.radius * math.cos(char_angle)
                cy = center + element.radius * math.sin(char_angle)

                rot_deg = (
                    math.degrees(char_angle + math.pi / 2)
                    + element.rotation
                    + flip_offset
                )

                bounds = skia.Rect()
                font.measureText(char, bounds=bounds)
                pivot_x = bounds.centerX() if bounds.width() > 0 else char_w / 2
                pivot_y = bounds.centerY() if bounds.height() > 0 else fallback_cy

                canvas.save()
                canvas.translate(cx, cy)
                canvas.rotate(rot_deg)
                canvas.drawString(char, -pivot_x, -pivot_y, font, paint)
                canvas.restore()

                cumulative += char_w + element.letter_spacing


    @staticmethod
    def _word_width(font: skia.Font, word: str, letter_spacing: float) -> float:
        base = font.measureText(word)
        extra = letter_spacing * (len(word) - 1) if len(word) > 1 else 0.0
        return base + extra