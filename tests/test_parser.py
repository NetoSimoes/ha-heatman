from __future__ import annotations

import pytest

from heatman.parser import ParameterParser


def _parser(items: list[dict], *, digits: int = 1, code: int = 3, min_span: int = 1, max_size: int = 20) -> ParameterParser:
    p = ParameterParser()
    p._items = items
    p._digits = digits
    p._code = code
    p._min_span = min_span
    p._max_size = max_size
    p._is_single_code = True
    p._lambda = lambda x, y, z: (y[1] - x[1] > min_span) or (y[1] - z[1] >= max_size)
    p._lambda_code_aware = lambda x, y, z: x[0] != y[0] or p._lambda(x, y, z)
    return p


def test_is_valid_enabled_requestable():
    p = ParameterParser()
    item = {"name": "Heating", "rule": 1, "platform": "switch"}
    assert p.is_valid(item)
    assert p.is_enabled(item)
    assert p.is_requestable(item)
    assert not p.is_valid({"rule": 1})
    assert not p.is_enabled({**item, "disabled": True})
    assert not p.is_requestable({**item, "rule": 0})


def test_is_scheduled_realtime_and_interval():
    p = ParameterParser()
    p._update_interval = 30
    assert p.is_scheduled({"realtime": True}, 7)
    assert p.is_scheduled({}, 0)
    assert p.is_scheduled({}, 30)
    assert not p.is_scheduled({}, 7)
    assert p.is_scheduled({"update_interval": 15}, 15)


def test_default_from_unit_of_measurement():
    p = ParameterParser()
    assert p.default_from_unit_of_measurement({"uom": "°C"}) is None
    assert p.default_from_unit_of_measurement({}) == ""
    assert p.default_from_unit_of_measurement({"unit_of_measurement": " "}) == ""


def test_in_range_and_do_validate():
    p = ParameterParser()
    assert p.in_range("t", 10, {"min": 0, "max": 20})
    assert not p.in_range("t", -1, {"min": 0})
    assert p.do_validate("t", 5, {"min": 0, "max": 10})
    assert not p.do_validate("t", 50, {"min": 0, "max": 10})


def test_do_validate_dev_and_invalidate_all():
    p = ParameterParser()
    p._previous_result["t"] = 10
    assert not p.do_validate("t", 40, {"dev": 5})
    with pytest.raises(ValueError, match="Invalidate complete dataset"):
        p.do_validate("t", 40, {"dev": 5, "invalidate_all": None})


def test_parse_unsigned_scale_and_bit():
    p = _parser([{"name": "Heating", "platform": "switch", "rule": 1, "key": "heating_switch", "registers": [0], "bit": 1, "code": 3}])
    result = p.process({(3, 0): [0b0000_0010]})
    assert result["heating_switch"][0] == 1
    p = _parser([{"name": "Temp", "platform": "sensor", "rule": 1, "key": "temp_sensor", "registers": [100], "scale": 0.1, "code": 3}])
    result = p.process({(3, 100): [215]})
    assert result["temp_sensor"][0] == 21.5


def test_parse_unsigned_missing_register_skips():
    p = _parser([{"name": "Temp", "platform": "sensor", "rule": 1, "key": "temp_sensor", "registers": [100], "code": 3}])
    assert p.process({(3, 0): [1]}) == {}


def test_parse_signed_negative():
    p = _parser([{"name": "Delta", "platform": "sensor", "rule": 2, "key": "delta_sensor", "registers": [10], "code": 3}])
    result = p.process({(3, 10): [0xFFFF]})
    assert result["delta_sensor"][0] == -1


def test_parse_signed_inverted():
    p = _parser([{"name": "Delta", "platform": "sensor", "rule": 2, "key": "delta_sensor", "registers": [10], "code": 3, "inverted": True}])
    result = p.process({(3, 10): [10]})
    assert result["delta_sensor"][0] == -10


def test_parse_ascii():
    p = _parser([{"name": "SN", "platform": "sensor", "rule": 5, "key": "sn_sensor", "registers": [1, 2], "code": 3}])
    result = p.process({(3, 1): [0x4142, 0x4344]})
    assert result["sn_sensor"][0] == "ABCD"


def test_parse_bits():
    p = _parser([{"name": "Flags", "platform": "sensor", "rule": 6, "key": "flags_sensor", "registers": [5], "code": 3}])
    result = p.process({(3, 5): [0x10]})
    assert result["flags_sensor"][0] == ["0x10"]


def test_parse_version():
    p = _parser([{"name": "FW", "platform": "sensor", "rule": 7, "key": "fw_sensor", "registers": [20], "code": 3}])
    result = p.process({(3, 20): [0x1234]})
    assert result["fw_sensor"][0] == "1.2.3.4"


def test_parse_datetime_three_registers():
    p = _parser([{"name": "Clock", "platform": "datetime", "rule": 8, "key": "clock_datetime", "registers": [1, 2, 3], "code": 3}])
    result = p.process({(3, 1): [0x1808, 0x1010, 0x0A00]})
    assert "/" in str(result["clock_datetime"][0])


def test_parse_time_single_register():
    p = _parser([{"name": "On", "platform": "time", "rule": 9, "key": "on_time", "registers": [30], "code": 3}])
    result = p.process({(3, 30): [1230]})
    assert result["on_time"][0] == "12:30"


def test_parse_raw():
    p = _parser([{"name": "Raw", "platform": "sensor", "rule": 10, "key": "raw_sensor", "registers": [1, 2], "code": 3}])
    result = p.process({(3, 1): [10, 20]})
    assert result["raw_sensor"][0] == [10, 20]


def test_parse_lookup():
    p = _parser([{
        "name": "Mode",
        "platform": "select",
        "rule": 1,
        "key": "mode_select",
        "registers": [1],
        "code": 3,
        "lookup": [{"key": 0, "value": "off"}, {"key": 1, "value": "heat"}, {"key": "default", "value": "?"}],
    }])
    result = p.process({(3, 1): [1]})
    assert result["mode_select"][0] == "heat"


def test_parse_uint32_low_word_first():
    p = _parser([{
        "name": "Energy",
        "platform": "sensor",
        "rule": 1,
        "key": "energy_sensor",
        "registers": [143, 144],
        "code": 3,
        "scale": 0.1,
    }])
    result = p.process({(3, 143): [0x0001, 0x0001]})
    assert result["energy_sensor"][0] == round((0x0001 + (0x0001 << 16)) * 0.1, 1)


def test_parse_mask():
    p = _parser([{"name": "Nibble", "platform": "sensor", "rule": 1, "key": "nibble_sensor", "registers": [0], "mask": 0x000F, "code": 3}])
    result = p.process({(3, 0): [0x12AB]})
    assert result["nibble_sensor"][0] == 0xB


def test_schedule_requests_does_not_span_register_two_hole():
    items = [
        {"name": "A", "platform": "switch", "rule": 1, "key": "a_switch", "registers": [0], "code": 3},
        {"name": "B", "platform": "switch", "rule": 1, "key": "b_switch", "registers": [1], "code": 3},
        {"name": "C", "platform": "number", "rule": 1, "key": "c_number", "registers": [3], "code": 3},
        {"name": "D", "platform": "number", "rule": 1, "key": "d_number", "registers": [11], "code": 3},
    ]
    p = _parser(items, min_span=1, max_size=20)
    requests = p.schedule_requests(0)
    spans = [(r["start"], r["end"]) for r in requests]
    assert (0, 11) not in spans
    assert (0, 1) in spans
    assert all(not (start < 2 < end) for start, end in spans)


def test_schedule_requests_respects_max_size():
    items = [{"name": f"R{i}", "platform": "sensor", "rule": 1, "key": f"r{i}_sensor", "registers": [i], "code": 3} for i in range(25)]
    p = _parser(items, min_span=1, max_size=10)
    requests = p.schedule_requests(0)
    assert all(r["count"] <= 10 for r in requests)


def test_schedule_requests_empty_when_nothing_due():
    items = [{"name": "A", "platform": "sensor", "rule": 1, "key": "a_sensor", "registers": [0], "code": 3, "update_interval": 30}]
    p = _parser(items)
    p._update_interval = 30
    assert p.schedule_requests(7) == []


def test_get_entity_descriptions_filters_attributes():
    p = _parser([
        {"name": "A", "platform": "sensor", "rule": 1, "key": "a_sensor", "registers": [0]},
        {"name": "B", "platform": "sensor", "rule": 1, "key": "b_sensor", "registers": [1], "attribute": True},
        {"name": "C", "platform": "switch", "rule": 1, "key": "c_switch", "registers": [2]},
    ])
    assert [i["key"] for i in p.get_entity_descriptions("sensor")] == ["a_sensor"]
    assert {i["key"] for i in p.get_entity_descriptions()} == {"a_sensor", "c_switch"}


def test_reset_clears_previous():
    p = ParameterParser()
    p._previous_result["t"] = 1
    p.reset()
    assert p._previous_result == {}


def test_custom_sensors_add_and_subtract():
    p = _parser([{
        "name": "Power",
        "platform": "sensor",
        "rule": 1,
        "key": "power_sensor",
        "registers": [1],
        "code": 3,
        "sensors": [
            {"registers": [1], "code": 3},
            {"registers": [2], "code": 3, "operator": "subtract"},
        ],
    }])
    result = p.process({(3, 1): [50, 10]})
    assert result["power_sensor"][0] == 40
