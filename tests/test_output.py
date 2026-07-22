import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from accessible_analyzer.output import create_run_directory, write_reports
from accessible_analyzer.reporting import build_report_data


class OutputTests(unittest.TestCase):
    def test_creates_distinct_timestamped_directories(self):
        with tempfile.TemporaryDirectory() as temp_directory:
            root = Path(temp_directory)
            moment = datetime(2026, 7, 21, 12, 30, tzinfo=timezone.utc)

            first = create_run_directory(base_directory=root, now=moment)
            second = create_run_directory(base_directory=root, now=moment)

            self.assertNotEqual(first, second)
            self.assertTrue(first.is_dir())
            self.assertTrue(second.is_dir())

    def test_writes_all_four_report_formats(self):
        report = build_report_data(
            {},
            metadata={"source": "file:///tmp/test.html", "analyzed_at": "now"},
        )
        with tempfile.TemporaryDirectory() as temp_directory:
            paths = write_reports(report, Path(temp_directory))

            self.assertEqual(set(paths), {"text", "markdown", "html", "json"})
            for path in paths.values():
                self.assertTrue(path.is_file())
                self.assertGreater(path.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
