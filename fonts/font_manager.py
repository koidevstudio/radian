from __future__ import annotations
from pathlib import Path
from functools import lru_cache
import skia


# Font directories — scanned once at startup

_FONT_DIRS: list[Path] = [
    Path("C:/Windows/Fonts"),
    Path("/usr/share/fonts"),
    Path("/usr/local/share/fonts"),
    Path("/System/Library/Fonts"),
    Path("/Library/Fonts"),
    Path.home() / ".fonts",
    Path("fonts/"),   # project-local fonts folder
]

_FONT_EXTENSIONS = {".ttf", ".otf", ".ttc"}
_INDEX: dict[str, dict[str, Path]] = {}
_INDEX_BUILT = False

def _parse_name_variant(stem: str) -> tuple[str, str]:

    known_variants = {
        "bold", "italic", "light", "thin", "medium",
        "semibold", "extrabold", "black", "regular",
        "condensed", "expanded", "oblique",
        "bolditalic", "lightitalic", "mediumitalic",
    }

    if "-" in stem:
        parts   = stem.split("-", 1)
        family  = parts[0].strip()
        variant = parts[1].strip()
    else:
        # Try to split CamelCase suffix: e.g. "RobotoRegular" → ("Roboto", "Regular")
        family  = stem
        variant = "Regular"
        for kv in sorted(known_variants, key=len, reverse=True):
            if stem.lower().endswith(kv):
                family  = stem[: len(stem) - len(kv)].strip()
                variant = stem[len(stem) - len(kv):].capitalize()
                break

    return family or stem, variant or "Regular"

def _build_index() -> None:
    global _INDEX, _INDEX_BUILT
    if _INDEX_BUILT:
        return

    for directory in _FONT_DIRS:
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if path.suffix.lower() not in _FONT_EXTENSIONS:
                continue
            family, variant = _parse_name_variant(path.stem)
            _INDEX.setdefault(family, {})[variant] = path

    _INDEX_BUILT = True


# Public API

@lru_cache(maxsize=256)
def get_typeface(family: str, variant: str = "Regular") -> skia.Typeface | None:
    """
    Returns a cached skia.Typeface for the given family plus variant.
    Falls back to 'Regular' if the variant is not found.
    Falls back to skia's default typeface if the family is not found.
    """
    _build_index()

    variants = _INDEX.get(family, {})

    # Exact variant match
    path = variants.get(variant)

    # Fallback: Regular
    if path is None:
        path = variants.get("Regular")

    # Fallback: first available variant
    if path is None and variants:
        path = next(iter(variants.values()))

    if path is not None:
        typeface = skia.Typeface.MakeFromFile(str(path))
        if typeface:
            return typeface

    # Last resort: let Skia resolve by name
    return skia.Typeface(family)


def get_font(family: str, size: float, variant: str = "Regular") -> skia.Typeface | None:
    """
    Convenience wrapper used by TypographyRenderer.
    Returns a Typeface (font size is applied by the caller via skia.Font).
    """
    return get_typeface(family, variant)


def list_available_fonts() -> list[str]:
    """Returns sorted list of font family names found on this system."""
    _build_index()
    return sorted(_INDEX.keys())


def list_variants(family: str) -> list[str]:
    """Returns available variants for a given font family."""
    _build_index()
    return sorted(_INDEX.get(family, {}).keys())