"""Parser specs."""

import pytest

from synergyscript import ast_nodes as ast
from synergyscript.errors import ParseError
from synergyscript.lexer import tokenize
from synergyscript.parser import parse


def test_onboard_builds_node():
    program = parse(tokenize("onboard quarters_left as 4"))
    stmt = program.body[0]
    assert isinstance(stmt, ast.Onboard)
    assert stmt.name == "quarters_left"


def test_arithmetic_precedence_with_keyword_operators():
    # leverage a with scale b by c  ==  a + (b * c)
    program = parse(tokenize("onboard x as leverage a with scale b by c"))
    expr = program.body[0].value
    assert isinstance(expr, ast.BinaryOp) and expr.op == "+"
    assert isinstance(expr.right, ast.BinaryOp) and expr.right.op == "*"


def test_unclosed_while_raises():
    with pytest.raises(ParseError):
        parse(tokenize("let's drill down while x > 0\n    run it up the flagpole x"))
