from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


# Primitives

@dataclass(frozen=True)
class Color:
    r: float
    g: float
    b: float

    def __post_init__(self) -> None:
        for ch in (self.r, self.g, self.b):
            if not (0.0 <= ch <= 1.0):
                raise ValueError(f"Color channel out of range: {ch}")

    @classmethod
    def black(cls) -> "Color":
        return cls(0.0, 0.0, 0.0)

    @classmethod
    def white(cls) -> "Color":
        return cls(1.0, 1.0, 1.0)

    @classmethod
    def from_hex(cls, hex_str: str) -> "Color":
        h = hex_str.lstrip("#")
        r, g, b = (int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))
        return cls(r, g, b)


# Enums

class MarkType(Enum):
    LINE   = auto()
    CIRCLE = auto()

class RenderMode(Enum):
    MARKS      = "marks"
    RINGS      = "rings"
    TYPOGRAPHY = "typography"


# Mask composed into every element

@dataclass
class Mask:
    enabled:  bool  = False
    angle:    float = 45.0   # degrees – aperture of the masked sector
    rotation: float = 0.0    # degrees – orientation of the sector

    def __post_init__(self) -> None:
        if not (0.0 < self.angle <= 360.0):
            raise ValueError(f"Mask angle must be (0, 360], got {self.angle}")


# Render configuration (canvas-level, not per-element)

@dataclass
class RenderConfig:
    canvas_size:  int   = 1920
    dpi:          int   = 300
    bg_color:     Color = field(default_factory=Color.white)
    transparent:  bool  = False


# Element base

@dataclass
class Element:
    id:          str
    label:       str
    color:       Color       = field(default_factory=Color.black)
    mask:        Mask        = field(default_factory=Mask)
    z_index:     int         = 0
    visible:     bool        = True
    render_mode: RenderMode  = RenderMode.MARKS   # overridden by subclasses


# Concrete element types

@dataclass
class MarksElement(Element):
    render_mode: RenderMode = field(default=RenderMode.MARKS, init=False)
    count:       int        = 60
    radius:      float      = 500.0   # px from canvas center
    length:      float      = 80.0    # tick length (LINE mode only)
    width:       float      = 4.0     # stroke width (LINE) - dot radius (CIRCLE)
    mark_type:   MarkType   = MarkType.LINE

@dataclass
class RingsElement(Element):
    render_mode: RenderMode = field(default=RenderMode.RINGS, init=False)
    radius:      float      = 500.0   # outer edge radius
    thickness:   float      = 80.0    # ring width (inner = radius - thickness)

@dataclass
class TypographyElement(Element):
    render_mode:    RenderMode = field(default=RenderMode.TYPOGRAPHY, init=False)
    text:           str        = ""
    font_family:    str        = ""
    font_variant:   str        = ""
    font_size:      float      = 40.0
    letter_spacing: float      = 0.0
    rotation:       float      = 0.0    # offset rotation in degrees
    flip:           bool       = False  # flip 180° (word order reversed)
    radius:         float      = 500.0  # placement radius from canvas center