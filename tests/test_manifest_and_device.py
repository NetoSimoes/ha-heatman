from __future__ import annotations

import json
from pathlib import Path

import yaml

from heatman.const import (
    DEPRECATION_SERVICE_WRITE_MULTIPLE_REGISTERS,
    DEPRECATION_SERVICE_WRITE_SINGLE_REGISTER,
    DOMAIN,
    SERVICE_READ_HOLDING_REGISTERS,
    SERVICE_READ_INPUT_REGISTERS,
    SERVICE_WRITE_MULTIPLE_REGISTERS,
    SERVICE_WRITE_SINGLE_REGISTER,
)
from heatman.device import DeviceState

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "custom_components" / "heatman"


def test_manifest_required_hacs_keys():
    manifest = json.loads((INTEGRATION / "manifest.json").read_text(encoding="utf-8"))
    for key in ("domain", "name", "documentation", "issue_tracker", "codeowners", "version"):
        assert key in manifest
    assert manifest["domain"] == DOMAIN
    assert manifest["config_flow"] is True
    assert "github.com/NetoSimoes/ha-heatman" in manifest["documentation"]


def test_hacs_json():
    hacs = json.loads((ROOT / "hacs.json").read_text(encoding="utf-8"))
    assert hacs["name"] == "Heatman"
    assert hacs["zip_release"] is True
    assert hacs["filename"] == "heatman.zip"
    assert hacs["hide_default_branch"] is True


def test_brand_icon_exists():
    assert (INTEGRATION / "brand" / "icon.png").is_file()


def test_services_yaml_covers_modbus_functions():
    services = yaml.safe_load((INTEGRATION / "services.yaml").read_text(encoding="utf-8"))
    for name in (
        SERVICE_READ_HOLDING_REGISTERS,
        SERVICE_READ_INPUT_REGISTERS,
        SERVICE_WRITE_SINGLE_REGISTER,
        SERVICE_WRITE_MULTIPLE_REGISTERS,
        DEPRECATION_SERVICE_WRITE_SINGLE_REGISTER,
        DEPRECATION_SERVICE_WRITE_MULTIPLE_REGISTERS,
    ):
        assert name in services
        assert "fields" in services[name]


def test_english_translations_config_flow():
    en = json.loads((INTEGRATION / "translations" / "en.json").read_text(encoding="utf-8"))
    assert "config" in en
    assert "step" in en["config"]


def test_device_state_lifecycle():
    state = DeviceState()
    assert state.print == "Disconnected"
    assert state.update(init=True) is True
    assert state.update() is False
    assert state.print == "Connected"
    assert state.update(exception=RuntimeError("x")) is False
    assert state.print == "Disconnected"
    assert state.update(exception=RuntimeError("x")) is True
    assert state.value == -1
