"""Token types and the Token record produced by the lexer."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    # Structural
    NEWLINE = auto()
    EOF = auto()

    # Literals
    NUMBER = auto()       # headcount, e.g. 42
    STRING = auto()       # messaging, e.g. "hello"
    IDENT = auto()        # variable / function name
    TRUE = auto()         # aligned
    FALSE = auto()        # blocked
    NULL = auto()         # tbd
    LAST_EMAIL = auto()   # per my last email (the last value run up the flagpole)

    # Variable statements
    TOUCH_BASE = auto()   # touch base
    ONBOARD = auto()      # onboard
    AS = auto()           # as
    TRANSITION = auto()   # transition
    TO = auto()           # to
    PRINT = auto()        # run it up the flagpole
    INPUT = auto()        # poll the stakeholders into

    # Arithmetic / logical operators
    LEVERAGE = auto()     # leverage   (+)
    WITH = auto()         # with
    TAKE = auto()         # take       (- , paired with OFFLINE_BY)
    OFFLINE_BY = auto()   # offline by
    SCALE = auto()        # scale      (*)
    STREAMLINE = auto()   # streamline (/)
    BY = auto()           # by
    AND = auto()          # and
    OR = auto()           # or

    # Comparison operators
    EQ = auto()           # ==
    NEQ = auto()          # !=
    GT = auto()           # >
    LT = auto()           # <
    GTE = auto()          # >=
    LTE = auto()          # <=

    # Punctuation
    COMMA = auto()        # ,

    # Control flow
    IF = auto()           # if we have bandwidth for
    ELIF = auto()         # pivot to
    ELSE = auto()         # pivot
    WHILE = auto()        # let's drill down while
    HARD_STOP = auto()    # hard stop
    CONTINUE = auto()     # push to next quarter
    END_BLOCK = auto()    # circle back

    # Functions
    FUNC_DEF = auto()     # schedule a meeting
    TAKING = auto()       # taking
    DELIVER = auto()      # deliver
    END_FUNC = auto()     # end meeting
    PING = auto()         # ping


@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str            # the source text matched
    line: int
    value: object = None   # literal value for NUMBER / STRING (else None)

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"Token({self.type.name}, {self.lexeme!r}, line={self.line})"
