from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "custom_components"))

from tests.ha_stub import install

install()

import pytest

from heatman.parser import ParameterParser


PROFILE_DIR = ROOT / "custom_components" / "heatman" / "heatpump_definitions"


@pytest.fixture
def profile_dir() -> str:
    return str(PROFILE_DIR) + "/"


@pytest.fixture
def parser() -> ParameterParser:
    return ParameterParser()
