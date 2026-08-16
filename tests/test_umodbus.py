from __future__ import annotations

import pytest

from heatman.pysolarman.umodbus.client import tcp
from heatman.pysolarman.umodbus.client.serial import rtu
from heatman.pysolarman.umodbus.client.serial.redundancy_check import get_crc, validate_crc
from heatman.pysolarman.umodbus.exceptions import IllegalDataAddressError, error_code_to_exception_map
from heatman.pysolarman.umodbus.functions import FUNCTION_CODE, pdu_to_function_code_or_raise_error


def test_tcp_read_holding_registers_roundtrip():
    req = tcp.read_holding_registers(1, 0, 2)
    assert req[6] == 1
    assert req[7] == 3
    pdu = bytes([0x03, 4, 0x00, 0x0A, 0x00, 0x14])
    resp = req[:2] + b"\x00\x00" + (1 + len(pdu)).to_bytes(2, "big") + bytes([1]) + pdu
    assert tcp.parse_response_adu(resp, req) == [10, 20]


def test_tcp_write_single_register_request():
    req = tcp.write_single_register(1, 7, 1)
    assert req[7] == 6
    assert int.from_bytes(req[8:10], "big") == 7
    assert int.from_bytes(req[10:12], "big") == 1


def test_rtu_crc_roundtrip():
    body = bytes([0x01, 0x03, 0x00, 0x00, 0x00, 0x01])
    frame = body + get_crc(body)
    validate_crc(frame)


def test_rtu_read_holding_registers_parse():
    req = rtu.read_holding_registers(1, 0, 1)
    resp_pdu_adu = bytes([0x01, 0x03, 0x02, 0x00, 0x2A])
    resp = resp_pdu_adu + get_crc(resp_pdu_adu)
    assert rtu.parse_response_adu(resp, req) == [42]


def test_exception_map_illegal_address():
    assert error_code_to_exception_map[2] is IllegalDataAddressError
    with pytest.raises(IllegalDataAddressError):
        pdu_to_function_code_or_raise_error(bytes([0x83, 0x02]))


def test_function_codes_include_holding_and_write():
    assert FUNCTION_CODE.READ_HOLDING_REGISTERS == 3
    assert FUNCTION_CODE.WRITE_SINGLE_REGISTER == 6
    assert FUNCTION_CODE.WRITE_MULTIPLE_REGISTERS == 16
