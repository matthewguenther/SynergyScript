"""Error types and internal control-flow signals.

Two distinct families live here:

* ``SynergyError`` and subclasses are *real* errors surfaced to the user with a
  line number (see README.md §7).
* The ``*Signal`` exceptions are an implementation convenience: the tree-walking
  interpreter uses exceptions to unwind ``deliver`` / ``hard stop`` /
  ``push to next quarter`` / top-level halt. They are never shown to the user.
"""

from __future__ import annotations


class SynergyError(Exception):
    """Base class for all user-facing errors. Carries an optional line number."""

    def __init__(self, message: str, line: int | None = None):
        self.message = message
        self.line = line
        super().__init__(f"Line {line}: {message}" if line else message)


class LexError(SynergyError):
    """Unrecognized token during lexing."""


class ParseError(SynergyError):
    """Malformed structure: unclosed block, stray terminator, bad statement."""


class RuntimeSynergyError(SynergyError):
    """Execution-time failure: undefined name, type mismatch, divide by zero, arity."""


# --- Internal control-flow signals (not user-facing) ------------------------

class ReturnSignal(Exception):
    """Raised by ``deliver`` to unwind to the active function call."""

    def __init__(self, value):
        self.value = value
        super().__init__()


class BreakSignal(Exception):
    """Raised by ``hard stop`` to break the innermost loop."""


class ContinueSignal(Exception):
    """Raised by ``push to next quarter`` to continue the innermost loop."""


class HaltSignal(Exception):
    """Raised by ``hard stop`` outside any loop to end the program successfully."""
