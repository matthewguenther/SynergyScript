"""HR linter specs. Marked xfail until HR is implemented."""

import pytest

from synergyscript.linter import lint

pytestmark = pytest.mark.xfail(reason="HR linter not yet implemented", strict=False)


def test_unclosed_block_is_flagged():
    warnings = lint("let's drill down while x > 0\n    run it up the flagpole x\n")
    assert any("circle back" in w.message for w in warnings)


def test_clean_program_has_no_warnings(hello_source):
    assert lint(hello_source) == []
