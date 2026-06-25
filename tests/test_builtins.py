"""builtins.render is implemented; verify corporate value display."""

from synergyscript.builtins import render


def test_render_booleans_use_corporate_words():
    assert render(True) == "aligned"
    assert render(False) == "blocked"


def test_render_null_is_tbd():
    assert render(None) == "tbd"


def test_render_numbers_and_strings():
    assert render(42) == "42"
    assert render("Hello World") == "Hello World"
