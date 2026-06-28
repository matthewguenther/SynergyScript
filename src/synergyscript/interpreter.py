"""The Intern — walks the AST and executes it.

Execution model (README.md §6):
  * Arithmetic phrases are pure expressions (no operand mutation).
  * ``deliver`` / ``hard stop`` / ``push to next quarter`` / top-level halt are
    implemented with the control-flow signal exceptions in ``errors.py``.
  * Scoping per ``environment.Environment``.
  * ``per my last email`` reads back the value most recently run up the flagpole;
    only ``run it up the flagpole`` updates that register, and it does so *after*
    printing, so ``run it up the flagpole per my last email`` echoes the prior
    value unchanged.
"""

from __future__ import annotations

from synergyscript import ast_nodes as ast
from synergyscript import builtins
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
        # "Institutional memory": the last value run up the flagpole. A single
        # program-wide register (not a scoped variable), seeded with tbd.
        self.last_email: object = None
        # How many loops we are nested inside *in the current call frame* — this
        # decides whether ``hard stop`` breaks a loop or halts the program.
        self.loop_depth = 0

    def run(self, program: ast.Program) -> None:
        """Execute a whole program. Pre-registers function defs, then runs the
        top-level body. A top-level ``hard stop`` raises HaltSignal, caught here.
        """
        for node in program.body:
            if isinstance(node, ast.FuncDef):
                self.functions[node.name] = node
        try:
            self.execute_block(program.body, self.globals)
        except HaltSignal:
            pass

    # --- statements ---------------------------------------------------------

    def execute(self, node: ast.Node, env: Environment) -> None:
        """Dispatch a statement node to its handler."""
        if isinstance(node, ast.TouchBase):
            return  # a polite no-op kickoff
        if isinstance(node, ast.Onboard):
            env.define(node.name, self.evaluate(node.value, env))
            return
        if isinstance(node, ast.Transition):
            env.assign(node.name, self.evaluate(node.value, env), node.line)
            return
        if isinstance(node, ast.Print):
            value = self.evaluate(node.value, env)
            builtins.run_it_up_the_flagpole(value)
            self.last_email = value  # update *after* sending the email
            return
        if isinstance(node, ast.Input):
            env.define(node.name, builtins.poll_the_stakeholders())
            return
        if isinstance(node, ast.If):
            self.execute_if(node, env)
            return
        if isinstance(node, ast.While):
            self.execute_while(node, env)
            return
        if isinstance(node, ast.FuncDef):
            self.functions[node.name] = node  # also registerable when nested
            return
        if isinstance(node, ast.Return):
            raise ReturnSignal(self.evaluate(node.value, env))
        if isinstance(node, ast.Break):
            # In a loop: break it. Outside any loop: halt the program.
            raise BreakSignal() if self.loop_depth > 0 else HaltSignal()
        if isinstance(node, ast.Continue):
            raise ContinueSignal()
        if isinstance(node, ast.Call):
            self.evaluate(node, env)  # call as a statement; result discarded
            return
        raise RuntimeSynergyError(
            f"Cannot execute {type(node).__name__}", getattr(node, "line", None)
        )

    def execute_block(self, body: list[ast.Node], env: Environment) -> None:
        for stmt in body:
            self.execute(stmt, env)

    def execute_if(self, node: ast.If, env: Environment) -> None:
        for condition, body in node.branches:
            if condition is None or self.is_truthy(self.evaluate(condition, env)):
                self.execute_block(body, env)
                return

    def execute_while(self, node: ast.While, env: Environment) -> None:
        self.loop_depth += 1
        try:
            while self.is_truthy(self.evaluate(node.condition, env)):
                try:
                    self.execute_block(node.body, env)
                except ContinueSignal:
                    continue
                except BreakSignal:
                    break
        finally:
            self.loop_depth -= 1

    # --- expressions --------------------------------------------------------

    def evaluate(self, node: ast.Node, env: Environment) -> object:
        """Evaluate an expression node to a runtime value."""
        if isinstance(node, ast.Literal):
            return node.value
        if isinstance(node, ast.Var):
            return env.get(node.name, node.line)
        if isinstance(node, ast.LastEmail):
            return self.last_email
        if isinstance(node, ast.BinaryOp):
            return self.eval_binary(node, env)
        if isinstance(node, ast.Call):
            args = [self.evaluate(arg, env) for arg in node.args]
            return self.call_function(node.name, args, node.line)
        raise RuntimeSynergyError(
            f"Cannot evaluate {type(node).__name__}", getattr(node, "line", None)
        )

    def eval_binary(self, node: ast.BinaryOp, env: Environment) -> object:
        op = node.op
        # Short-circuiting logical operators evaluate the right side lazily.
        if op == "and":
            return self.is_truthy(self.evaluate(node.left, env)) and self.is_truthy(
                self.evaluate(node.right, env)
            )
        if op == "or":
            return self.is_truthy(self.evaluate(node.left, env)) or self.is_truthy(
                self.evaluate(node.right, env)
            )

        left = self.evaluate(node.left, env)
        right = self.evaluate(node.right, env)
        line = node.line

        if op == "==":
            return left == right
        if op == "!=":
            return left != right
        if op in ("<", ">", "<=", ">="):
            return self._compare(op, left, right, line)
        if op == "+":
            return self._arith(lambda a, b: a + b, left, right, line, "leverage")
        if op == "-":
            return self._arith(lambda a, b: a - b, left, right, line, "take offline")
        if op == "*":
            return self._arith(lambda a, b: a * b, left, right, line, "scale")
        if op == "/":
            if right == 0:
                raise RuntimeSynergyError(
                    "Cannot streamline by 0 — division by zero", line
                )
            return self._arith(lambda a, b: a // b, left, right, line, "streamline")
        raise RuntimeSynergyError(f"Unknown operator {op!r}", line)

    @staticmethod
    def _compare(op: str, left: object, right: object, line: int) -> bool:
        try:
            if op == "<":
                return left < right
            if op == ">":
                return left > right
            if op == "<=":
                return left <= right
            return left >= right
        except TypeError:
            raise RuntimeSynergyError(
                f"Cannot compare {builtins.render(left)!r} and {builtins.render(right)!r}",
                line,
            ) from None

    @staticmethod
    def _arith(fn, left: object, right: object, line: int, what: str) -> object:
        # Booleans are not headcounts, even though Python treats them as ints.
        if isinstance(left, bool) or isinstance(right, bool):
            raise RuntimeSynergyError(f"Cannot {what} a buy-in (true/false) value", line)
        try:
            return fn(left, right)
        except TypeError:
            raise RuntimeSynergyError(
                f"Cannot {what} {builtins.render(left)!r} and {builtins.render(right)!r}"
                " — incompatible types",
                line,
            ) from None

    def call_function(self, name: str, args: list[object], line: int) -> object:
        """Bind args to a fresh local scope (parent = globals) and run the body.
        Returns the ``deliver``ed value, or None (``tbd``) if the function falls
        off the end. Validates arity.
        """
        func = self.functions.get(name)
        if func is None:
            raise RuntimeSynergyError(f"No meeting scheduled named '{name}'", line)
        if len(args) != len(func.params):
            raise RuntimeSynergyError(
                f"'{name}' expected {len(func.params)} input(s) but got {len(args)}",
                line,
            )

        local = Environment(parent=self.globals)
        for param, value in zip(func.params, args):
            local.define(param, value)

        # Each call frame has its own loop nesting; a ``hard stop`` inside a
        # function but outside a loop halts the program, it does not break the
        # caller's loop.
        saved_depth = self.loop_depth
        self.loop_depth = 0
        try:
            self.execute_block(func.body, local)
            return None
        except ReturnSignal as ret:
            return ret.value
        finally:
            self.loop_depth = saved_depth

    # --- helpers ------------------------------------------------------------

    @staticmethod
    def is_truthy(value: object) -> bool:
        """Truthiness coercion for conditions (README.md §6)."""
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, int):
            return value != 0
        if isinstance(value, str):
            return value != ""
        return True


def run_source(source: str) -> None:
    """Lex -> parse -> interpret a string of SynergyScript. Used by the CLI."""
    from synergyscript.lexer import tokenize
    from synergyscript.parser import parse

    Interpreter().run(parse(tokenize(source)))
