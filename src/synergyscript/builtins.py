"""Built-in I/O for the interpreter.

``run it up the flagpole`` -> stdout, ``poll the stakeholders into`` -> stdin.
Indirected through here (rather than calling print()/input() inline) so tests can
capture output and feed input without monkeypatching the interpreter.
"""

from __future__ import annotations

import sys
from typing import Callable


def render(value: object) -> str:
    """Display form of a SynergyScript value.

    Booleans render as their corporate keywords; ``tbd`` (None) renders as 'tbd'.
    """
    if value is True:
        return "aligned"
    if value is False:
        return "blocked"
    if value is None:
        return "tbd"
    return str(value)


def run_it_up_the_flagpole(value: object, out: Callable[[str], None] = print) -> None:
    out(render(value))


def poll_the_stakeholders(prompt: str = "", stream=sys.stdin) -> str:
    """Read one line of input as a ``messaging`` (string), newline stripped."""
    if prompt:
        sys.stdout.write(prompt)
    return stream.readline().rstrip("\n")
