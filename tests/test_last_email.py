"""Specs for ``per my last email`` — the implicit last-value register.

``per my last email`` reads back the value most recently run up the flagpole.
Only ``run it up the flagpole`` writes to it, and only *after* printing.
"""

from synergyscript import ast_nodes as ast
from synergyscript.interpreter import run_source
from synergyscript.lexer import tokenize
from synergyscript.parser import parse
from synergyscript.tokens import TokenType as T


# --- lexing -----------------------------------------------------------------

def test_phrase_is_a_single_token():
    # Four words, one token — not four identifiers.
    types = [t.type for t in tokenize("per my last email") if t.type is not T.NEWLINE]
    assert types == [T.LAST_EMAIL]


def test_phrase_still_just_text_inside_a_comment():
    assert [t.type for t in tokenize("// per my last email: hi")] == []


# --- parsing ----------------------------------------------------------------

def test_parses_to_last_email_node():
    program = parse(tokenize("onboard takeaway as per my last email"))
    assert isinstance(program.body[0].value, ast.LastEmail)


# --- evaluating -------------------------------------------------------------

def test_reads_back_the_last_flagpole(capsys):
    run_source(
        "run it up the flagpole 42\n"
        "run it up the flagpole per my last email\n"
        "hard stop\n"
    )
    assert capsys.readouterr().out.split() == ["42", "42"]


def test_can_be_captured_and_built_upon(capsys):
    run_source(
        "run it up the flagpole scale 7 by 6\n"      # reports 42
        "run it up the flagpole leverage per my last email with 8\n"  # 50
        "onboard final_number as per my last email\n"  # captures 50
        "run it up the flagpole final_number\n"
        "hard stop\n"
    )
    assert capsys.readouterr().out.split() == ["42", "50", "50"]


def test_is_tbd_before_anything_is_flagpoled(capsys):
    run_source("run it up the flagpole per my last email\nhard stop\n")
    assert capsys.readouterr().out.strip() == "tbd"


def test_echoing_does_not_mutate_the_register(capsys):
    run_source(
        "run it up the flagpole 7\n"
        "run it up the flagpole per my last email\n"
        "run it up the flagpole per my last email\n"
        "hard stop\n"
    )
    assert capsys.readouterr().out.split() == ["7", "7", "7"]


def test_only_flagpole_updates_it_not_onboard(capsys):
    # `onboard`/`transition` assign values but do not "send an email".
    run_source(
        "run it up the flagpole 1\n"
        "onboard noise as 999\n"
        "transition noise to 12345\n"
        "run it up the flagpole per my last email\n"
        "hard stop\n"
    )
    assert capsys.readouterr().out.split() == ["1", "1"]


def test_demo_script_runs(capsys, scripts_dir):
    run_source((scripts_dir / "per_my_last_email.corp").read_text(encoding="utf-8"))
    assert capsys.readouterr().out.split() == ["42", "50", "50"]
