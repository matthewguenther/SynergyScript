"""The Intern — walks the AST and executes it.

Execution model (README.md §6):
  * Arithmetic phrases are pure expressions (no operand mutation).
  * ``deliver`` / ``hard stop`` / ``push to next quarter`` / top-level halt are
    implemented with the control-flow signal exceptions in ``errors.py``.
  * Scoping per ``environment.Environment``.

Scaffold: dispatch and visitor skeletons are present; node logic is TODO.
"""

from __future__ import annotations

from synergyscript import ast_nodes as ast
from synergyscript.environment import Environment
from synergyscript.errors import (
    BreakSignal,
    ContinueSignal,
    HaltSignal,
    ReturnSignal,
    RuntimeSynergyError,
)


class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self.functions: dict[str, ast.FuncDef] = {}

    def run(self, program: ast.Program) -> None:
        """Execute a whole program. Pre-registers function defs, then runs the
        top-level body. A top-level ``hard stop`` raises HaltSignal, caught here.
        """
        raise NotImplementedError("Interpreter.run: hoist functions, exec body")

    # --- statements ---------------------------------------------------------

    def execute(self, node: ast.Node, env: Environment) -> None:
        """Dispatch a statement node to its handler."""
        raise NotImplementedError

    def execute_block(self, body: list[ast.Node], env: Environment) -> None:
        for stmt in body:
            self.execute(stmt, env)

    # --- expressions --------------------------------------------------------

    def evaluate(self, node: ast.Node, env: Environment) -> object:
        """Evaluate an expression node to a runtime value."""
        raise NotImplementedError

    def call_function(self, name: str, args: list[object], line: int) -> object:
        """Bind args to a fresh local scope (parent = globals) and run the body.
        Returns the ``deliver``ed value, or None (``tbd``) if the function falls
        off the end. Validates arity.
        """
        raise NotImplementedError

    # --- helpers ------------------------------------------------------------

    @staticmethod
    def is_truthy(value: object) -> bool:
        """Truthiness coercion for conditions (README.md §6)."""
        raise NotImplementedError


def run_source(source: str) -> None:
    """Lex -> parse -> interpret a string of SynergyScript. Used by the CLI."""
    from synergyscript.lexer import tokenize
    from synergyscript.parser import parse

    Interpreter().run(parse(tokenize(source)))
