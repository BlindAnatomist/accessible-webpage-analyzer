"""Pure report construction and rendering functions."""

from __future__ import annotations

import html
import json
from collections import Counter
from collections.abc import Mapping, Sequence
from typing import Any

from . import SCHEMA_VERSION


def _counts(items: Sequence[Mapping[str, Any]], key: str) -> dict[str, int]:
    values = (str(item.get(key, "unknown")) for item in items)
    return dict(Counter(values))


def _most_common(counts: Mapping[str, int], fallback: str) -> str:
    if not counts:
        return fallback
    return max(counts, key=counts.get)


def build_report_data(
    styles_by_section: Mapping[str, Sequence[Mapping[str, Any]]],
    *,
    metadata: Mapping[str, Any],
    warnings: Sequence[str] = (),
) -> dict[str, Any]:
    """Build a stable, renderer-independent report model."""

    sections: list[dict[str, Any]] = []
    spoken_phrases: list[str] = []

    for section_name, raw_items in styles_by_section.items():
        items = [dict(item) for item in raw_items]
        fonts = _counts(items, "font")
        sizes = _counts(items, "size")
        colors = _counts(items, "color")
        backgrounds = _counts(items, "bgColor")
        layouts = _counts(items, "display")

        top_font = _most_common(fonts, "the default font")
        top_color = _most_common(colors, "the default text color")
        top_background = _most_common(backgrounds, "no explicit background")
        layout_modes = ", ".join(layouts) if layouts else "normal flow"
        spoken = (
            f"The {section_name} region contains {len(items)} elements and most often uses "
            f"{top_font}, with {top_color} on {top_background}, laid out using {layout_modes}."
        )
        spoken_phrases.append(spoken)

        sections.append(
            {
                "name": str(section_name),
                "element_count": len(items),
                "fonts": fonts,
                "sizes": sizes,
                "text_colors": colors,
                "background_colors": backgrounds,
                "layouts": layouts,
                "elements": items,
                "spoken_summary": spoken,
            }
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "metadata": dict(metadata),
        "warnings": [str(warning) for warning in warnings],
        "sections": sections,
        "spoken_summary": " ".join(spoken_phrases),
    }


def _format_counts(counts: Mapping[str, int]) -> str:
    if not counts:
        return "None recorded"
    return ", ".join(f"{name} ({count})" for name, count in counts.items())


def _escape_markdown(value: Any) -> str:
    text = html.escape(str(value), quote=False)
    for character in r"\`*_{}[]()#+-.!|":
        text = text.replace(character, f"\\{character}")
    return text


def render_text(report: Mapping[str, Any]) -> str:
    metadata = report.get("metadata", {})
    lines = [
        "Webpage Layout Report",
        f"Source: {metadata.get('source', 'unknown')}",
        f"Analyzed at: {metadata.get('analyzed_at', 'unknown')}",
        f"Schema version: {report.get('schema_version', 'unknown')}",
    ]

    warnings = report.get("warnings", [])
    if warnings:
        lines.append("\nWarnings")
        lines.extend(f"- {warning}" for warning in warnings)

    for section in report.get("sections", []):
        lines.extend(
            [
                f"\n--- {str(section['name']).upper()} ({section['element_count']} elements) ---",
                f"Fonts: {_format_counts(section['fonts'])}",
                f"Sizes: {_format_counts(section['sizes'])}",
                f"Text colors: {_format_counts(section['text_colors'])}",
                f"Backgrounds: {_format_counts(section['background_colors'])}",
                f"Layouts: {_format_counts(section['layouts'])}",
            ]
        )

    lines.extend(["\nSpoken layout summary", str(report.get("spoken_summary", ""))])
    return "\n".join(lines)


def render_markdown(report: Mapping[str, Any]) -> str:
    metadata = report.get("metadata", {})
    escape = _escape_markdown
    lines = [
        "# Webpage Layout Report",
        "",
        f"- Source: {escape(metadata.get('source', 'unknown'))}",
        f"- Analyzed at: {escape(metadata.get('analyzed_at', 'unknown'))}",
        f"- Schema version: {escape(report.get('schema_version', 'unknown'))}",
    ]

    warnings = report.get("warnings", [])
    if warnings:
        lines.extend(["", "## Warnings"])
        lines.extend(f"- {escape(warning)}" for warning in warnings)

    for section in report.get("sections", []):
        lines.extend(
            [
                "",
                f"## {escape(section['name'])}",
                f"- Elements: {escape(section['element_count'])}",
                f"- Fonts: {escape(_format_counts(section['fonts']))}",
                f"- Sizes: {escape(_format_counts(section['sizes']))}",
                f"- Text colors: {escape(_format_counts(section['text_colors']))}",
                f"- Backgrounds: {escape(_format_counts(section['background_colors']))}",
                f"- Layouts: {escape(_format_counts(section['layouts']))}",
            ]
        )

    lines.extend(["", "## Spoken layout summary", escape(report.get("spoken_summary", ""))])
    return "\n".join(lines) + "\n"


def render_html(report: Mapping[str, Any]) -> str:
    metadata = report.get("metadata", {})
    escape = lambda value: html.escape(str(value), quote=True)

    parts = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>Webpage Layout Report</title>",
        "</head>",
        "<body>",
        "<main>",
        "<h1>Webpage Layout Report</h1>",
        "<dl>",
        f"<dt>Source</dt><dd>{escape(metadata.get('source', 'unknown'))}</dd>",
        f"<dt>Analyzed at</dt><dd>{escape(metadata.get('analyzed_at', 'unknown'))}</dd>",
        f"<dt>Schema version</dt><dd>{escape(report.get('schema_version', 'unknown'))}</dd>",
        "</dl>",
    ]

    warnings = report.get("warnings", [])
    if warnings:
        parts.extend(["<section>", "<h2>Warnings</h2>", "<ul>"])
        parts.extend(f"<li>{escape(warning)}</li>" for warning in warnings)
        parts.extend(["</ul>", "</section>"])

    for section in report.get("sections", []):
        parts.extend(
            [
                "<section>",
                f"<h2>{escape(section['name'])}</h2>",
                "<ul>",
                f"<li>Elements: {escape(section['element_count'])}</li>",
                f"<li>Fonts: {escape(_format_counts(section['fonts']))}</li>",
                f"<li>Sizes: {escape(_format_counts(section['sizes']))}</li>",
                f"<li>Text colors: {escape(_format_counts(section['text_colors']))}</li>",
                f"<li>Backgrounds: {escape(_format_counts(section['background_colors']))}</li>",
                f"<li>Layouts: {escape(_format_counts(section['layouts']))}</li>",
                "</ul>",
                "</section>",
            ]
        )

    parts.extend(
        [
            "<section>",
            "<h2>Spoken layout summary</h2>",
            f"<p>{escape(report.get('spoken_summary', ''))}</p>",
            "</section>",
            "</main>",
            "</body>",
            "</html>",
        ]
    )
    return "\n".join(parts) + "\n"


def render_json(report: Mapping[str, Any]) -> str:
    return json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
