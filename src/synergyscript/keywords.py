"""The canonical corporate-vocabulary -> token mapping.

This is the single source of truth shared by the lexer and parser (README.md
§4). Keep it here; do not duplicate the table elsewhere.

The lexer must apply *longest-phrase-first* matching, so ``PHRASES_LONGEST_FIRST``
exposes the keyword phrases ordered by word count (descending) for convenient
greedy matching.
"""

from __future__ import annotations

from synergyscript.tokens import TokenType as T

# Multi-word and single-word keyword phrases (lowercase, space-normalized).
# Value literals (aligned / blocked / tbd) are included so they are reserved.
PHRASE_TOKENS: dict[str, T] = {
    # variable statements
    "touch base": T.TOUCH_BASE,
    "onboard": T.ONBOARD,
    "as": T.AS,
    "transition": T.TRANSITION,
    "to": T.TO,
    "run it up the flagpole": T.PRINT,
    "poll the stakeholders into": T.INPUT,
    # operators
    "leverage": T.LEVERAGE,
    "with": T.WITH,
    "take": T.TAKE,
    "offline by": T.OFFLINE_BY,
    "scale": T.SCALE,
    "streamline": T.STREAMLINE,
    "by": T.BY,
    "and": T.AND,
    "or": T.OR,
    # control flow
    "if we have bandwidth for": T.IF,
    "pivot to": T.ELIF,
    "pivot": T.ELSE,
    "let's drill down while": T.WHILE,
    "hard stop": T.HARD_STOP,
    "push to next quarter": T.CONTINUE,
    "circle back": T.END_BLOCK,
    # functions
    "schedule a meeting": T.FUNC_DEF,
    "taking": T.TAKING,
    "deliver": T.DELIVER,
    "end meeting": T.END_FUNC,
    "ping": T.PING,
    # literal values
    "aligned": T.TRUE,
    "blocked": T.FALSE,
    "tbd": T.NULL,
    # institutional memory — the last value run up the flagpole
    "per my last email": T.LAST_EMAIL,
}

# Symbol operators. Match longest first (handled by SYMBOLS_LONGEST_FIRST).
SYMBOL_TOKENS: dict[str, T] = {
    "==": T.EQ,
    "!=": T.NEQ,
    ">=": T.GTE,
    "<=": T.LTE,
    ">": T.GT,
    "<": T.LT,
    ",": T.COMMA,
}

# Every individual word that appears in any keyword phrase. NOTE: appearing here
# does not by itself make a word unusable as a name. Longest-phrase-first lexing
# means only words that are *themselves* a standalone single-word phrase (``as``,
# ``to``, ``with``, ``onboard``, …) are unavailable as identifiers; a word that
# only ever shows up inside a multi-word phrase — e.g. ``a`` in
# ``schedule a meeting`` — is a perfectly legal name (``fibonacci.corp`` uses
# ``a`` and ``b``). Kept as a reference set for tooling such as HR.
RESERVED_WORDS: frozenset[str] = frozenset(
    word for phrase in PHRASE_TOKENS for word in phrase.split()
)

# Keyword phrases ordered longest-first (by word count, then char length) so the
# lexer can try the most specific match before falling back.
PHRASES_LONGEST_FIRST: list[tuple[str, T]] = sorted(
    PHRASE_TOKENS.items(),
    key=lambda kv: (len(kv[0].split()), len(kv[0])),
    reverse=True,
)

SYMBOLS_LONGEST_FIRST: list[tuple[str, T]] = sorted(
    SYMBOL_TOKENS.items(), key=lambda kv: len(kv[0]), reverse=True
)
