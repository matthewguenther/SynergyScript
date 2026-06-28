"""AST node definitions. The parser builds these; the interpreter walks them.

Every node carries the source ``line`` it began on for error reporting. Nodes
are plain dataclasses with no behavior — evaluation lives in ``interpreter.py``.
"""

from __future__ import annotations

from dataclasses import dataclass, field


class Node:
    """Base class for all AST nodes."""


# --- Program & statements ---------------------------------------------------

@dataclass
class Program(Node):
    body: list[Node] = field(default_factory=list)


@dataclass
class TouchBase(Node):           # touch base  (no-op kickoff)
    line: int = 0


@dataclass
class Onboard(Node):             # onboard NAME as EXPR
    name: str
    value: "Node"
    line: int = 0


@dataclass
class Transition(Node):          # transition NAME to EXPR
    name: str
    value: "Node"
    line: int = 0


@dataclass
class Print(Node):               # run it up the flagpole EXPR
    value: "Node"
    line: int = 0


@dataclass
class Input(Node):               # poll the stakeholders into NAME
    name: str
    line: int = 0


@dataclass
class If(Node):                  # if / pivot to / pivot
    # branches: list of (condition, body); the bare ``pivot`` else has cond=None
    branches: list[tuple["Node | None", list[Node]]]
    line: int = 0


@dataclass
class While(Node):               # let's drill down while COND ... circle back
    condition: "Node"
    body: list[Node]
    line: int = 0


@dataclass
class FuncDef(Node):             # schedule a meeting NAME taking PARAMS ... end meeting
    name: str
    params: list[str]
    body: list[Node]
    line: int = 0


@dataclass
class Return(Node):              # deliver EXPR
    value: "Node"
    line: int = 0


@dataclass
class Break(Node):               # hard stop
    line: int = 0


@dataclass
class Continue(Node):            # push to next quarter
    line: int = 0


# --- Expressions ------------------------------------------------------------

@dataclass
class Literal(Node):             # NUMBER / STRING / aligned / blocked / tbd
    value: object
    line: int = 0


@dataclass
class Var(Node):                 # identifier reference
    name: str
    line: int = 0


@dataclass
class LastEmail(Node):           # per my last email — the last value run up the flagpole
    line: int = 0


@dataclass
class BinaryOp(Node):            # leverage/take/scale/streamline, comparisons, and/or
    op: str                      # e.g. "+", "-", "*", "/", "==", ">", "and"
    left: "Node"
    right: "Node"
    line: int = 0


@dataclass
class Call(Node):                # ping NAME with ARGS  (statement or expression)
    name: str
    args: list["Node"]
    line: int = 0
