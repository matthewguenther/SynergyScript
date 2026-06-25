"""Environment is fully implemented, so these run for real."""

import pytest

from synergyscript.environment import Environment
from synergyscript.errors import RuntimeSynergyError


def test_define_and_get():
    env = Environment()
    env.define("quarters_left", 4)
    assert env.get("quarters_left") == 4


def test_assign_updates_nearest_binding():
    glob = Environment()
    glob.define("status", "pending")
    local = Environment(parent=glob)
    local.assign("status", "KPIs Met")
    assert glob.get("status") == "KPIs Met"
    assert "status" not in local.values


def test_assign_to_undeclared_raises():
    with pytest.raises(RuntimeSynergyError):
        Environment().assign("ghost", 1)


def test_get_undefined_raises():
    with pytest.raises(RuntimeSynergyError):
        Environment().get("ghost")
