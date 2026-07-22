import json
import unittest

from accessible_analyzer.reporting import (
    build_report_data,
    render_html,
    render_json,
    render_markdown,
    render_text,
)


class ReportingTests(unittest.TestCase):
    def setUp(self):
        self.malicious_font = '$(touch /tmp/should-not-run) <script>alert("x")</script>'
        self.report = build_report_data(
            {
                "main": [
                    {
                        "tag": "p",
                        "font": self.malicious_font,
                        "size": "16px",
                        "color": "black",
                        "bgColor": "white",
                        "display": "block",
                    }
                ]
            },
            metadata={
                "source": "https://example.com/?value=<unsafe>",
                "analyzed_at": "2026-07-21T12:00:00+00:00",
            },
            warnings=["Example <warning>"],
        )

    def test_html_escapes_page_derived_values(self):
        html = render_html(self.report)

        self.assertNotIn("<script>alert", html)
        self.assertIn("&lt;script&gt;alert", html)
        self.assertIn("&lt;unsafe&gt;", html)
        self.assertIn("Example &lt;warning&gt;", html)

    def test_markdown_escapes_page_derived_markup(self):
        markdown = render_markdown(self.report)

        self.assertNotIn("<script>alert", markdown)
        self.assertIn("&lt;script&gt;alert", markdown)
        self.assertNotIn("[unsafe](javascript:alert(1))", markdown)

    def test_json_includes_schema_and_metadata(self):
        payload = json.loads(render_json(self.report))

        self.assertEqual(payload["schema_version"], "1.0")
        self.assertEqual(payload["metadata"]["source"], "https://example.com/?value=<unsafe>")
        self.assertEqual(payload["sections"][0]["element_count"], 1)

    def test_text_report_retains_source_identity_and_warning(self):
        text = render_text(self.report)

        self.assertIn("Source: https://example.com/?value=<unsafe>", text)
        self.assertIn("Example <warning>", text)
        self.assertIn("MAIN (1 elements)", text)


if __name__ == "__main__":
    unittest.main()
