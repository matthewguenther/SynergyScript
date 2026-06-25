"""The ``synergy`` command-line tool.

    synergy execute path/to/file.corp   # run a program (The Intern)
    synergy HR      path/to/file.corp   # lint with HR

CLI plumbing is implemented; it delegates to the lexer / parser / interpreter /
linter, which are still being built out. Running a command today will surface a
NotImplementedError from the relevant stage — that is the expected next step.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from synergyscript import __version__
from synergyscript.errors import SynergyError


def _read_corp(path_str: str) -> str:
    path = Path(path_str)
    if path.suffix != ".corp":
        print(f"synergy: expected a .corp file, got '{path.name}'", file=sys.stderr)
        raise SystemExit(2)
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"synergy: cannot read '{path}': {exc}", file=sys.stderr)
        raise SystemExit(2)


def _cmd_execute(path: str) -> int:
    from synergyscript.interpreter import run_source

    try:
        run_source(_read_corp(path))
    except SynergyError as exc:
        print(f"[Blocker] {exc}", file=sys.stderr)
        return 1
    return 0


def _cmd_hr(path: str) -> int:
    from synergyscript.linter import lint

    warnings = lint(_read_corp(path))
    for warning in warnings:
        print(warning)
    if not warnings:
        print("[HR] Great alignment. No action items at this time.")
    return 1 if warnings else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="synergy", description="SynergyScript — the corporate esoteric language."
    )
    parser.add_argument("--version", action="version", version=f"synergy {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_exec = sub.add_parser("execute", help="run a .corp program")
    p_exec.add_argument("file")

    p_hr = sub.add_parser("HR", help="lint a .corp program with HR")
    p_hr.add_argument("file")

    args = parser.parse_args(argv)

    if args.command == "execute":
        return _cmd_execute(args.file)
    if args.command == "HR":
        return _cmd_hr(args.file)
    parser.error(f"unknown command {args.command!r}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
