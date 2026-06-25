"""The Recruiter — turns raw .corp source into a stream of tokens.

Responsibilities (README.md §3):
  * Longest-phrase-first matching of the corporate vocabulary (``keywords.py``).
  * Word-boundary awareness ("as" never matches inside "assets").
  * Number / string / identifier literals.
  * Symbol operators (== != >= <= > < ,).
  * "//" line comments (discarded).
  * NEWLINE as a statement separator; blank runs collapse to one.

Scaffold: the matching algorithm is described per-method but not yet implemented.
"""

from __future__ import annotations

from synergyscript.errors import LexError
from synergyscript.keywords import (
    PHRASES_LONGEST_FIRST,
    SYMBOLS_LONGEST_FIRST,
)
from synergyscript.tokens import Token, TokenType


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.tokens: list[Token] = []

    def tokenize(self) -> list[Token]:
        """Scan the whole source and return tokens, terminated by EOF.

        Loop: skip inline whitespace and comments, then at each position try, in
        order: newline -> string literal -> number literal -> symbol operator
        -> keyword phrase (longest first) -> identifier. Unmatched input raises
        ``LexError``.
        """
        raise NotImplementedError("Lexer.tokenize: implement the scan loop")

    # --- individual matchers (return a Token or None) -----------------------

    def _match_keyword_phrase(self) -> Token | None:
        """Try each phrase in ``PHRASES_LONGEST_FIRST``, honoring word boundaries."""
        raise NotImplementedError

    def _match_symbol(self) -> Token | None:
        """Try each operator in ``SYMBOLS_LONGEST_FIRST`` (longest first)."""
        raise NotImplementedError

    def _match_number(self) -> Token | None:
        """Match an integer literal -> Token(NUMBER, value=int)."""
        raise NotImplementedError

    def _match_string(self) -> Token | None:
        """Match a double-quoted string -> Token(STRING, value=str)."""
        raise NotImplementedError

    def _match_identifier(self) -> Token | None:
        """Match [A-Za-z_][A-Za-z0-9_]* that is not a RESERVED_WORD."""
        raise NotImplementedError


def tokenize(source: str) -> list[Token]:
    """Convenience wrapper used by the parser and tests."""
    return Lexer(source).tokenize()
