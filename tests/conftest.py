"""Shared test fixtures."""

from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"


@pytest.fixture
def scripts_dir() -> Path:
    return SCRIPTS_DIR


@pytest.fixture
def hello_source() -> str:
    return (SCRIPTS_DIR / "hello.corp").read_text(encoding="utf-8")
