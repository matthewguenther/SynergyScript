"""HR — the passive-aggressive static linter (README.md §7).

HR does *not* execute the program. It scans tokens / AST and reports warnings in
the voice of a Human Resources business partner who would like to align on your
choices. v1 checks:
  * blocks opened but never closed (circle back / end meeting)
  * a terminator with no matching opener
  * variables onboarded but never used
  * transition to a name that was never onboarded

Scaffold: ``check`` returns a list of warnings; the rule bodies are TODO.
"""

from __future__ import annotations

from dataclasses import dataclass

from synergyscript.tokens import Token


@dataclass
class HRWarning:
    line: int
    message: str

    def __str__(self) -> str:
        return f"[HR Warning] Line {self.line}: {self.message}"


class HR:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.warnings: list[HRWarning] = []

    def check(self) -> list[HRWarning]:
        """Run all static checks and return the collected warnings."""
        raise NotImplementedError("HR.check: run the lint rules")

    def _check_unclosed_blocks(self) -> None:
        raise NotImplementedError

    def _check_stray_terminators(self) -> None:
        raise NotImplementedError

    def _check_unused_variables(self) -> None:
        raise NotImplementedError

    def _check_undeclared_transition(self) -> None:
        raise NotImplementedError


def lint(source: str) -> list[HRWarning]:
    """Lex ``source`` and run HR. Used by the CLI's ``HR`` subcommand."""
    from synergyscript.lexer import tokenize

    return HR(tokenize(source)).check()
