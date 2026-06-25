"""Runtime scopes for variables and functions.

Scoping rules (README.md §6): the top level is global. Each function call
gets a fresh local scope whose parent is the *global* scope (no closures in v1).
``define`` binds in the current scope; ``assign`` updates the nearest existing
binding; reads search current then parent.

This module is fully implemented — it is small and unambiguous.
"""

from __future__ import annotations

from synergyscript.errors import RuntimeSynergyError


class Environment:
    def __init__(self, parent: "Environment | None" = None):
        self.parent = parent
        self.values: dict[str, object] = {}

    def define(self, name: str, value: object) -> None:
        """``onboard`` — bind a name in this scope (declaration)."""
        self.values[name] = value

    def assign(self, name: str, value: object, line: int | None = None) -> None:
        """``transition`` — update the nearest existing binding."""
        env: "Environment | None" = self
        while env is not None:
            if name in env.values:
                env.values[name] = value
                return
            env = env.parent
        raise RuntimeSynergyError(
            f"Cannot transition '{name}' — it was never onboarded", line
        )

    def get(self, name: str, line: int | None = None) -> object:
        env: "Environment | None" = self
        while env is not None:
            if name in env.values:
                return env.values[name]
            env = env.parent
        raise RuntimeSynergyError(f"Undefined variable '{name}'", line)

    def has(self, name: str) -> bool:
        env: "Environment | None" = self
        while env is not None:
            if name in env.values:
                return True
            env = env.parent
        return False
