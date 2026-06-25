"""End-to-end interpreter specs. Marked xfail until the Intern is implemented."""

import pytest

from synergyscript.interpreter import run_source

pytestmark = pytest.mark.xfail(reason="Interpreter not yet implemented", strict=False)


def test_hello_world(capsys, hello_source):
    run_source(hello_source)
    assert capsys.readouterr().out.strip() == "Hello World"


def test_countdown(capsys, scripts_dir):
    run_source((scripts_dir / "q3_earnings.corp").read_text(encoding="utf-8"))
    out = capsys.readouterr().out.split()
    assert out[:4] == ["4", "3", "2", "1"]
    assert "KPIs" in out


def test_fibonacci(capsys, scripts_dir):
    run_source((scripts_dir / "fibonacci.corp").read_text(encoding="utf-8"))
    nums = [int(x) for x in capsys.readouterr().out.split()]
    assert nums == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_arithmetic_is_pure_expression(capsys):
    # `leverage count with 1` must NOT mutate count; only `transition` does.
    run_source(
        "onboard count as 5\n"
        "run it up the flagpole leverage count with 1\n"
        "run it up the flagpole count\n"
        "hard stop\n"
    )
    assert capsys.readouterr().out.split() == ["6", "5"]
