"""The Recruiter — turns raw .corp source into a stream of tokens.

Responsibilities (README.md §3):
  * Longest-phrase-first matching of the corporate vocabulary (``keywords.py``).
  * Word-boundary awareness ("as" never matches inside "assets").
  * Number / string / identifier literals.
  * Symbol operators (== != >= <= > < ,).
  * "//" line comments (discarded).
  * NEWLINE as a statement separator; blank runs collapse to one.
"""

from __future__ import annotations

from synergyscript.errors import LexError
from synergyscript.keywords import (
    PHRASES_LONGEST_FIRST,
    SYMBOLS_LONGEST_FIRST,
)
from synergyscript.tokens import Token, TokenType

# Characters that make up an identifier (and therefore a "word" for boundary
# checks). A keyword phrase only counts as a match if it is not butting up
# against one of these — that is how ``as`` avoids firing inside ``assets``.
_IDENT_START = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
_IDENT_CONT = _IDENT_START + "0123456789"
_INLINE_WS = " \t\r"


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
        src = self.source
        n = len(src)
        while self.pos < n:
            ch = src[self.pos]

            # Inline whitespace is purely cosmetic (README §2).
            if ch in _INLINE_WS:
                self.pos += 1
                continue

            # "//" comment: discard to end of line (the newline itself stays).
            if src.startswith("//", self.pos):
                while self.pos < n and src[self.pos] != "\n":
                    self.pos += 1
                continue

            # Newlines separate statements; collapse blank runs to one token.
            if ch == "\n":
                self._add_newline()
                self.pos += 1
                self.line += 1
                continue

            token = (
                self._match_string()
                or self._match_number()
                or self._match_symbol()
                or self._match_keyword_phrase()
                or self._match_identifier()
            )
            if token is None:
                snippet = src[self.pos : self.pos + 12]
                raise LexError(f"Unrecognized input near {snippet!r}", self.line)
            self.tokens.append(token)

        # A trailing NEWLINE carries no statement; drop it. The EOF sentinel the
        # parser peeks at is the parser's concern, not part of the token stream.
        if self.tokens and self.tokens[-1].type is TokenType.NEWLINE:
            self.tokens.pop()
        return self.tokens

    # --- newline bookkeeping ------------------------------------------------

    def _add_newline(self) -> None:
        """Emit a single NEWLINE, collapsing leading/repeated blank lines."""
        if self.tokens and self.tokens[-1].type is not TokenType.NEWLINE:
            self.tokens.append(Token(TokenType.NEWLINE, "\\n", self.line))

    # --- individual matchers (return a Token or None) -----------------------

    def _at_word_boundary(self, end: int) -> bool:
        """True if the character at ``end`` does not continue an identifier."""
        return end >= len(self.source) or self.source[end] not in _IDENT_CONT

    def _match_keyword_phrase(self) -> Token | None:
        """Try each phrase in ``PHRASES_LONGEST_FIRST``, honoring word boundaries.

        Phrase words may be separated by any run of inline whitespace, and the
        match must end on a word boundary so ``pivot`` never fires inside
        ``pivots`` and ``as`` never fires inside ``assets``.
        """
        src = self.source
        for phrase, ttype in PHRASES_LONGEST_FIRST:
            end = self._match_phrase_words(phrase)
            if end is not None and self._at_word_boundary(end):
                lexeme = src[self.pos : end]
                self.pos = end
                return Token(ttype, lexeme, self.line)
        return None

    def _match_phrase_words(self, phrase: str) -> int | None:
        """If ``phrase`` matches at the cursor, return the end index, else None."""
        src = self.source
        n = len(src)
        i = self.pos
        for w, word in enumerate(phrase.split()):
            if w > 0:  # allow cosmetic whitespace between phrase words
                while i < n and src[i] in _INLINE_WS:
                    i += 1
            if src[i : i + len(word)] != word:
                return None
            i += len(word)
        return i

    def _match_symbol(self) -> Token | None:
        """Try each operator in ``SYMBOLS_LONGEST_FIRST`` (longest first)."""
        src = self.source
        for symbol, ttype in SYMBOLS_LONGEST_FIRST:
            if src.startswith(symbol, self.pos):
                self.pos += len(symbol)
                return Token(ttype, symbol, self.line)
        return None

    def _match_number(self) -> Token | None:
        """Match an integer literal -> Token(NUMBER, value=int)."""
        src = self.source
        start = self.pos
        i = start
        while i < len(src) and src[i].isdigit():
            i += 1
        if i == start:
            return None
        lexeme = src[start:i]
        self.pos = i
        return Token(TokenType.NUMBER, lexeme, self.line, value=int(lexeme))

    def _match_string(self) -> Token | None:
        """Match a double-quoted string -> Token(STRING, value=str)."""
        src = self.source
        if src[self.pos] != '"':
            return None
        i = self.pos + 1
        while i < len(src) and src[i] != '"':
            if src[i] == "\n":  # strings do not span lines
                raise LexError("Unterminated messaging (string)", self.line)
            i += 1
        if i >= len(src):
            raise LexError("Unterminated messaging (string)", self.line)
        value = src[self.pos + 1 : i]
        lexeme = src[self.pos : i + 1]
        self.pos = i + 1
        return Token(TokenType.STRING, lexeme, self.line, value=value)

    def _match_identifier(self) -> Token | None:
        """Match [A-Za-z_][A-Za-z0-9_]* as a name.

        Standalone keyword phrases (including single words like ``as`` / ``to``)
        are already consumed by ``_match_keyword_phrase`` before we get here, so a
        word that survives to this point is genuinely a name. Words that only ever
        appear *inside* a multi-word phrase — like ``a`` in ``schedule a meeting``
        — are therefore perfectly legal names (``fibonacci.corp`` relies on ``a``
        and ``b``).
        """
        src = self.source
        if src[self.pos] not in _IDENT_START:
            return None
        i = self.pos + 1
        while i < len(src) and src[i] in _IDENT_CONT:
            i += 1
        name = src[self.pos : i]
        self.pos = i
        return Token(TokenType.IDENT, name, self.line)


def tokenize(source: str) -> list[Token]:
    """Convenience wrapper used by the parser and tests."""
    return Lexer(source).tokenize()
