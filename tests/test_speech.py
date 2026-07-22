import unittest
from types import SimpleNamespace

from accessible_analyzer.speech import speak


class SpeechTests(unittest.TestCase):
    def test_passes_untrusted_text_as_one_argument_without_a_shell(self):
        calls = []

        def fake_runner(arguments, **kwargs):
            calls.append((arguments, kwargs))
            return SimpleNamespace(returncode=0)

        untrusted = '$(touch /tmp/should-not-run); echo "unsafe"'
        result = speak(untrusted, runner=fake_runner)

        self.assertEqual(result, 0)
        self.assertEqual(calls[0][0], ["say", untrusted])
        self.assertNotIn("shell", calls[0][1])

    def test_empty_text_does_not_start_a_process(self):
        called = False

        def fake_runner(*args, **kwargs):
            nonlocal called
            called = True
            return SimpleNamespace(returncode=0)

        self.assertEqual(speak("   ", runner=fake_runner), 0)
        self.assertFalse(called)


if __name__ == "__main__":
    unittest.main()
