from __future__ import annotations

from ipaddress import IPv4Address
from pathlib import Path

import pytest
import voluptuous as vol

from heatman.common import (
    all_equals,
    all_same,
    async_listdir,
    bulk_delete,
    bulk_inherit,
    bulk_migrate,
    bulk_safe_delete,
    concat_hex,
    create_request,
    div_mod,
    ensure_list,
    ensure_list_safe_len,
    entity_key,
    filter_by_keys,
    format,
    from_bit_index,
    get_addr_value,
    get_battery_cycles,
    get_battery_power_capacity,
    get_code,
    get_current_file_name,
    get_number,
    get_or_def,
    get_request_code,
    get_start_addr,
    get_tuple,
    getipaddress,
    group_when,
    ilen,
    lookup_value,
    process_profile,
    protected,
    replace_first,
    slugify,
    split_p16b,
    strepr,
    to_dict,
    unwrap,
    _listdir,
)
from heatman.const import DOMAIN, REQUEST_CODE, REQUEST_CODE_ALT, REQUEST_COUNT, REQUEST_END, REQUEST_START
from heatman.common import build_device_info, retry, throttle


def test_protected_rejects_none():
    with pytest.raises(vol.Invalid):
        protected(None, "missing")


def test_protected_returns_value():
    assert protected("host", "missing") == "host"


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("profile.yaml", "yaml"),
        ("midea_mthermal_a.yaml", "yaml"),
        ("noext", "noext"),
        ("", ""),
    ],
)
def test_get_current_file_name(value, expected):
    assert get_current_file_name(value) == expected


def test_listdir_missing_returns_empty(tmp_path: Path):
    assert _listdir(str(tmp_path / "missing"), "", ("yaml", "yml")) == []


def test_listdir_files_and_prefix(tmp_path: Path):
    (tmp_path / "a.yaml").write_text("x: 1\n")
    (tmp_path / "b.yml").write_text("x: 1\n")
    (tmp_path / "skip.txt").write_text("nope")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "c.yaml").write_text("x: 1\n")
    assert _listdir(str(tmp_path), "", ("yaml", "yml")) == ["a.yaml", "b.yml"]
    assert _listdir(str(tmp_path), "custom/", ("yaml", "yml")) == ["custom/a.yaml", "custom/b.yml"]


@pytest.mark.asyncio
async def test_async_listdir(tmp_path: Path):
    (tmp_path / "midea_mthermal_a.yaml").write_text("info: {}\n")
    assert await async_listdir(str(tmp_path)) == ["midea_mthermal_a.yaml"]


def test_getipaddress_literal():
    assert getipaddress("192.168.1.10") == IPv4Address("192.168.1.10")


def test_to_dict_and_filter_by_keys():
    keys = to_dict("a", "b")
    assert keys == {"a": "a", "b": "b"}
    assert filter_by_keys({"a": 1, "b": 2, "c": 3}, keys) == {"a": 1, "b": 2}


def test_bulk_inherit_skips_existing_and_none():
    target = {"a": 1}
    source = {"a": 9, "b": 2, "c": None}
    assert bulk_inherit(target, source) == {"a": 1, "b": 2}


def test_bulk_inherit_selected_keys():
    target = {}
    source = {"a": 1, "b": 2}
    assert bulk_inherit(target, source, "b") == {"b": 2}


def test_bulk_migrate():
    target = {}
    source = {"old_host": "1.2.3.4"}
    assert bulk_migrate(target, source, {"host": "old_host"}) == {"host": "1.2.3.4"}


def test_bulk_delete_and_safe_delete():
    target = {"a": 1, "b": 2, "host": "x", "inverter_host": "y"}
    bulk_delete(target, "a")
    assert "a" not in target
    bulk_safe_delete(target, {"host": "inverter_host"})
    assert "inverter_host" not in target
    assert "host" in target


def test_ensure_list_and_safe_len():
    assert ensure_list(1) == [1]
    assert ensure_list([1, 2]) == [1, 2]
    assert ensure_list_safe_len([1, 2]) == ([1, 2], 2)
    assert ensure_list_safe_len({"a": 1}) == ([{"a": 1}], 1)
    assert ensure_list_safe_len({}) == ([{}], 0)
    assert ensure_list_safe_len("x") == (["x"], 0)


def test_create_request():
    req = create_request(3, 0, 11)
    assert req == {REQUEST_CODE: 3, REQUEST_START: 0, REQUEST_END: 11, REQUEST_COUNT: 12}


def test_process_profile_passthrough_and_redirect(monkeypatch):
    from heatman import common

    assert process_profile("midea_mthermal_a.yaml", {}) == "midea_mthermal_a.yaml"
    monkeypatch.setitem(common.PROFILE_REDIRECT, "old.yaml", "new.yaml")
    assert process_profile("old.yaml", {}) == "new.yaml"
    params = {}
    monkeypatch.setitem(common.PROFILE_REDIRECT, "old.yaml", "new.yaml:mod=1")
    assert process_profile("old.yaml", params) == "new.yaml"
    assert params["mod"] == 1


def test_all_equals_all_same():
    assert all_equals([1, 1, 1], 1)
    assert not all_equals([1, 2], 1)
    assert all_same([3, 3, 3])
    assert not all_same([3, 4])


def test_group_when_splits_on_gap():
    regs = [(3, 0), (3, 1), (3, 3), (3, 4)]
    groups = list(group_when(regs, lambda x, y, z: y[1] - x[1] > 1))
    assert groups == [[(3, 0), (3, 1)], [(3, 3), (3, 4)]]


def test_group_when_single_item():
    assert list(group_when([(3, 0)], lambda *_: True)) == [[(3, 0)]]


def test_format_and_strepr():
    assert format("ok") == "ok"
    assert format(b"\x01\x02") == "01 02"
    assert strepr("hi") == "hi"
    assert strepr("") == "''"


def test_unwrap_list_and_overflow():
    source = {"model": ["A", "B"]}
    unwrap(source, "model", 0)
    assert source["model"] == "A"
    source = {"model": ["A", "B"]}
    unwrap(source, "model", 9)
    assert source["model"] == "B"


def test_slugify_and_entity_key():
    assert slugify("Heating", "switch") == "heating_switch"
    assert entity_key({"name": "DHW Setpoint", "platform": "number"}) == "dhw_setpoint_number"


def test_get_code_int_and_mapping():
    assert get_code({"code": 3}, "read") == 3
    assert get_code({"code": {"read": 4, "write": 6}}, "write") == 6
    assert get_code({}, "read", 3) == 3


def test_get_start_addr_and_value():
    data = {(3, 10): [100, 101, 102]}
    assert get_start_addr(data, 3, 11) == (3, 10)
    assert get_addr_value(data, 3, 11) == 101
    assert get_addr_value(data, 3, 99) is None
    assert get_start_addr(data, 4, 10) is None


def test_ilen_replace_first_get_or_def():
    assert ilen([1, 2]) == 2
    assert ilen(5) == 1
    assert replace_first("Heat Pump", "Solius") == "Solius Pump"
    assert get_or_def({"a": 0}, "a", 5) == 5
    assert get_or_def({"a": 3}, "a", 5) == 3


def test_from_bit_index_and_lookup():
    assert from_bit_index(1) == 2
    assert from_bit_index([0, 2]) == 5
    lookup = [{"key": 0, "value": "off"}, {"key": 1, "value": "heat"}, {"key": "default", "value": "unknown"}]
    assert lookup_value(1, lookup) == "heat"
    assert lookup_value(99, lookup) == "unknown"


def test_get_number_rounding():
    assert get_number(10.0) == 10
    assert get_number(10.26, 1) == 10.3
    assert get_number(10.2, 1) == 10.2


def test_get_request_code_aliases():
    assert get_request_code({"code": 3}) == 3
    assert get_request_code({"mb_functioncode": 4}) == 4
    assert get_request_code({}, 3) == 3


def test_get_tuple_and_battery_helpers():
    assert get_tuple((1, 2)) == 1
    assert get_tuple(None) is None
    assert get_battery_power_capacity(100, 48) == 4.8
    assert get_battery_cycles(9.6, 100, 48) == 2


def test_split_p16b_div_mod_concat_hex():
    assert list(split_p16b(0x12345678)) == [0x5678, 0x1234]
    assert div_mod(125, 100) == (1, 25)
    assert concat_hex((1, 2)) == 0x0102


def test_build_device_info_from_profile_info():
    info = build_device_info("abc", "SN1", "aabbccddeeff", "192.168.1.1", {"manufacturer": "Midea", "model": "M-Thermal A Series"}, "Solius")
    assert info["manufacturer"] == "Midea"
    assert info["model"] == "M-Thermal A Series"
    assert info["name"] == "Solius"
    assert (DOMAIN, "abc") in info["identifiers"]
    assert (DOMAIN, "SN1") in info["identifiers"]


def test_build_device_info_from_filename():
    info = build_device_info("abc", None, None, "host", {"filename": "midea_mthermal_a.yaml"}, "Heat Pump")
    assert info["manufacturer"] == "Midea"
    assert "Mthermal" in info["model"] or "mthermal" in info["model"].lower()


@pytest.mark.asyncio
async def test_retry_retries_once():
    calls = {"n": 0}

    @retry()
    async def flaky():
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("boom")
        return "ok"

    assert await flaky() == "ok"
    assert calls["n"] == 2


@pytest.mark.asyncio
async def test_retry_ignore_does_not_retry():
    @retry(ignore=(ValueError,))
    async def boom():
        raise ValueError("no")

    with pytest.raises(ValueError):
        await boom()


@pytest.mark.asyncio
async def test_throttle_zero_delay():
    @throttle(0)
    async def ping():
        return 1

    assert await ping() == 1
    assert await ping() == 1
