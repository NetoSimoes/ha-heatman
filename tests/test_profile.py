from __future__ import annotations

from pathlib import Path

import yaml

from heatman.parser import ParameterParser


PROFILE = Path(__file__).resolve().parents[1] / "custom_components" / "heatman" / "heatpump_definitions" / "midea_mthermal_a.yaml"


def test_profile_yaml_loads():
    profile = yaml.safe_load(PROFILE.read_text(encoding="utf-8"))
    assert profile["info"]["manufacturer"] == "Midea"
    assert profile["default"]["code"] == 3
    assert profile["default"]["min_span"] == 1
    assert profile["default"]["max_size"] == 20
    assert profile["parameters"]


def test_profile_items_have_name_rule_registers():
    profile = yaml.safe_load(PROFILE.read_text(encoding="utf-8"))
    keys = []
    for group in profile["parameters"]:
        assert "items" in group
        for item in group["items"]:
            assert "name" in item
            assert "rule" in item
            assert "registers" in item
            keys.append((item["name"], item.get("platform", "sensor")))
    assert len(keys) == len(set(keys))


async def test_parser_init_from_mthermal_profile(profile_dir: str):
    parser = await ParameterParser().init(profile_dir, "midea_mthermal_a.yaml", {"mod": 0})
    assert parser.info["manufacturer"] == "Midea"
    assert parser.info["filename"] == "midea_mthermal_a.yaml"
    assert parser._min_span == 1
    assert parser._max_size == 20
    assert parser._code == 3
    descriptions = parser.get_entity_descriptions()
    assert any(d["name"] == "Heating" for d in descriptions)
    assert any(d["name"] == "DHW" for d in descriptions)
    requests = parser.schedule_requests(0)
    assert requests
    assert all(r["count"] <= 20 for r in requests)
    assert not any(r["start"] == 0 and r["end"] >= 11 for r in requests)


async def test_parser_process_heating_bit_from_profile(profile_dir: str):
    parser = await ParameterParser().init(profile_dir, "midea_mthermal_a.yaml", {"mod": 0})
    heating = next(d for d in parser.get_entity_descriptions("switch") if d["name"] == "Heating")
    data = {(3, 0): [0b0000_0010]}
    result = parser.process(data)
    assert heating["key"] in result
