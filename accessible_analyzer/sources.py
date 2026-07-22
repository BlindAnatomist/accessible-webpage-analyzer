"""Source-address validation helpers."""

from __future__ import annotations

from urllib.parse import urlparse

_ALLOWED_SCHEMES = {"http", "https", "file"}


def validate_source(source: str) -> str:
    """Validate and normalize a webpage source accepted by ChromeDriver."""

    normalized = source.strip()
    if not normalized:
        raise ValueError("A webpage URL or local file address is required.")

    parsed = urlparse(normalized)
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        allowed = ", ".join(sorted(_ALLOWED_SCHEMES))
        raise ValueError(f"Unsupported URL scheme. Allowed schemes: {allowed}.")

    if parsed.scheme.lower() in {"http", "https"} and not parsed.netloc:
        raise ValueError("Webpage URLs must include a host name.")

    if parsed.scheme.lower() == "file" and not parsed.path:
        raise ValueError("Local file addresses must include a path.")

    return normalized
