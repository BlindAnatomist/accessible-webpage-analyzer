"""Safe optional platform speech."""

from __future__ import annotations

import subprocess
from collections.abc import Callable
from typing import Any


def speak(
    text: str,
    *,
    executable: str = "say",
    runner: Callable[..., Any] = subprocess.run,
) -> int:
    """Speak text without invoking a shell."""

    if not text.strip():
        return 0

    completed = runner(
        [executable, text],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    return int(completed.returncode)
