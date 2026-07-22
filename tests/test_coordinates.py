import unittest

from accessible_analyzer.coordinates import normalize_rect


class NormalizeRectTests(unittest.TestCase):
    def test_adds_scroll_offsets_and_preserves_viewport_values(self):
        result = normalize_rect(
            {"top": -20, "left": 15, "width": 100, "height": 40},
            scroll_x=5,
            scroll_y=200,
        )

        self.assertEqual(result["top"], 180.0)
        self.assertEqual(result["left"], 20.0)
        self.assertEqual(result["right"], 120.0)
        self.assertEqual(result["bottom"], 220.0)
        self.assertEqual(result["viewport_top"], -20.0)
        self.assertEqual(result["viewport_left"], 15.0)

    def test_rejects_incomplete_rectangle(self):
        with self.assertRaises(ValueError):
            normalize_rect({"top": 0, "left": 0, "width": 10})


if __name__ == "__main__":
    unittest.main()
