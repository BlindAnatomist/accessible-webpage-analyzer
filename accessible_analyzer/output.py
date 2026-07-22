"""Output-directory and report-writing helpers."""

from __future__ import annotations

import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .reporting import render_html, render_json, render_markdown, render_text


def default_output_root() -> Path:
    return Path(tempfile.gettempdir()) / "accessible-webpage-analyzer"


def create_run_directory(
    *,
    base_directory: Path | None = None,
    now: datetime | None = None,
) -> Path:
    root = base_directory or default_output_root()
    moment = now or datetime.now(timezone.utc)
    stamp = moment.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    candidate = root / stamp
    suffix = 1
    while candidate.exists():
        candidate = root / f"{stamp}-{suffix}"
        suffix += 1
    candidate.mkdir(parents=True, exist_ok=False)
    return candidate


def write_reports(report: Mapping[str, Any], output_directory: Path) -> dict[str, Path]:
    paths = {
        "text": output_directory / "webpage_report.txt",
        "markdown": output_directory / "webpage_report.md",
        "html": output_directory / "webpage_report.html",
        "json": output_directory / "webpage_report.json",
    }
    paths["text"].write_text(render_text(report), encoding="utf-8")
    paths["markdown"].write_text(render_markdown(report), encoding="utf-8")
    paths["html"].write_text(render_html(report), encoding="utf-8")
    paths["json"].write_text(render_json(report), encoding="utf-8")
    return paths
