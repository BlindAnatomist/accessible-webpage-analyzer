import unittest

from accessible_analyzer.sources import validate_source


class SourceValidationTests(unittest.TestCase):
    def test_accepts_http_https_and_file_sources(self):
        self.assertEqual(validate_source(" https://example.com/a "), "https://example.com/a")
        self.assertEqual(validate_source("http://localhost:3000"), "http://localhost:3000")
        self.assertEqual(validate_source("file:///tmp/test.html"), "file:///tmp/test.html")

    def test_rejects_non_web_schemes(self):
        with self.assertRaises(ValueError):
            validate_source("javascript:alert(1)")

    def test_rejects_web_url_without_host(self):
        with self.assertRaises(ValueError):
            validate_source("https:///missing-host")


if __name__ == "__main__":
    unittest.main()
