"""Lexer specs.

Run a single test:  pytest tests/test_lexer.py::test_phrase_longest_match
"""

from synergyscript.lexer import tokenize
from synergyscript.tokens import TokenType as T


def _types(source):
    return [t.type for t in tokenize(source) if t.type is not T.NEWLINE]


def test_phrase_longest_match():
    # "run it up the flagpole" is ONE token, not five identifiers.
    types = _types('run it up the flagpole "hi"')
    assert types[0] is T.PRINT
    assert types[1] is T.STRING


def test_pivot_to_beats_pivot():
    assert _types("pivot to aligned")[0] is T.ELIF
    assert _types("pivot")[0] is T.ELSE


def test_word_boundary_not_inside_identifier():
    # "assets" must not be lexed as the keyword "as" + "sets".
    types = _types("onboard assets as 5")
    assert types == [T.ONBOARD, T.IDENT, T.AS, T.NUMBER]


def test_subtraction_is_two_tokens():
    assert _types("take x offline by 1") == [T.TAKE, T.IDENT, T.OFFLINE_BY, T.NUMBER]


def test_comment_is_discarded():
    assert _types("// per my last email: hi") == []
