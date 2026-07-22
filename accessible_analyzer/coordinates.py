"""Coordinate normalization helpers."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

_REQUIRED_KEYS = ("top", "left", "width", "height")


def normalize_rect(
    rect: Mapping[str, Any],
    *,
    scroll_x: float = 0.0,
    scroll_y: float = 0.0,
) -> dict[str, float]:
    """Return stable document coordinates plus original viewport coordinates."""

    missing = [key for key in _REQUIRED_KEYS if key not in rect]
    if missing:
        raise ValueError(f"Rectangle is missing required keys: {', '.join(missing)}")

    viewport_top = float(rect["top"])
    viewport_left = float(rect["left"])
    width = float(rect["width"])
    height = float(rect["height"])

    return {
        "top": viewport_top + float(scroll_y),
        "left": viewport_left + float(scroll_x),
        "right": viewport_left + float(scroll_x) + width,
        "bottom": viewport_top + float(scroll_y) + height,
        "width": width,
        "height": height,
        "viewport_top": viewport_top,
        "viewport_left": viewport_left,
    }
