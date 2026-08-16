from __future__ import annotations

import struct

import pytest

from heatman.pysolarman import PROTOCOL, FrameError, Solarman
from heatman.pysolarman.umodbus.client import tcp


def _client(transport: str = "modbus_tcp") -> Solarman:
    return Solarman("192.168.1.50", 502, transport, 0, 1, 5)


def _mbap_pdu(pdu: bytes, unit: int = 1, transaction: int = 1) -> bytes:
    return struct.pack(">HHHB", transaction, 0, len(pdu) + 1, unit) + pdu


def test_init_creates_rx_buf_for_modbus_tcp():
    client = _client()
    assert hasattr(client, "_rx_buf")
    assert client.transport == "modbus_tcp"
    assert client._handle_frame is None
    assert client._get_response == client._parse_adu_from_tcp_response


def test_init_solarman_tcp_uses_protocol_handler():
    client = _client("tcp")
    assert client._handle_frame is not None
    assert client._get_response == client._parse_adu_from_sol_response


def test_init_rtu_uses_rtu_parser():
    client = _client("modbus_rtu")
    assert client._get_response == client._parse_adu_from_rtu_response


def test_checksum_and_response_code():
    assert Solarman._get_response_code(0x45) == 0x15
    frame = bytes.fromhex("01 02 03")
    assert Solarman._calculate_checksum(frame) == (1 + 2 + 3) & 0xFF


def test_serial_int_and_bytes():
    client = _client()
    client.serial = 0
    assert client.serial == 0
    assert client.serial_bytes == PROTOCOL.PLACEHOLDER3
    client.serial = 3000000000
    assert client.serial == 3000000000
    client.serial = b"\x01\x02\x03\x04"
    assert client.serial == 0x04030201


def test_sequence_number_increments():
    client = _client()
    first = client.sequence_number
    second = client.sequence_number
    assert first != 0
    assert second == ((first + 1) & 0xFF)


def test_protocol_header_and_trailer():
    client = _client("tcp")
    header = client._protocol_header(10, PROTOCOL.CONTROL_CODE.REQUEST, b"\x01\x00")
    assert header.startswith(PROTOCOL.START)
    trailer = client._protocol_trailer(header)
    assert trailer.endswith(PROTOCOL.END)


def test_extract_frames_reassembles_split_modbus_tcp():
    client = _client()
    pdu = bytes([0x03, 24]) + (b"\x00\x01" * 12)
    full = _mbap_pdu(pdu)
    assert len(full) == 6 + (len(pdu) + 1)
    assert client._extract_frames(full[:20]) == []
    frames = client._extract_frames(full[20:])
    assert frames == [full]
    assert client._rx_buf == b""


def test_extract_frames_two_complete_adus():
    client = _client()
    a = _mbap_pdu(bytes([0x03, 2, 0x00, 0x01]), transaction=1)
    b = _mbap_pdu(bytes([0x03, 2, 0x00, 0x02]), transaction=2)
    frames = client._extract_frames(a + b)
    assert frames == [a, b]


def test_extract_frames_drops_invalid_mbap_length():
    client = _client()
    garbage = b"\x00\x01\x00\x00\xff\xff\x01"
    assert client._extract_frames(garbage) == []
    assert client._rx_buf == b""


def test_extract_frames_rtu_passthrough():
    client = _client("modbus_rtu")
    blob = b"\x01\x03\x02\x00\x01\x79\x84"
    assert client._extract_frames(blob) == [blob]


def test_extract_frames_solarman_passthrough():
    client = _client("tcp")
    blob = b"\xa5\x0a\x00"
    assert client._extract_frames(blob) == [blob]


def test_received_frame_rejects_non_start():
    client = _client("tcp")
    client._sequence_number = 1
    assert client._received_frame_is_valid(b"\x00\x01") is False


def test_enqueue_ignores_when_not_waiting():
    client = _client()
    client._enqueue_frame(b"\x00")
    assert client._data_queue.empty()


def test_enqueue_replaces_queued_frame():
    client = _client()
    client._data_event.set()
    client._enqueue_frame(b"\x01")
    client._data_event.set()
    client._enqueue_frame(b"\x02")
    assert client._data_queue.get_nowait() == b"\x02"


@pytest.mark.asyncio
async def test_parse_tcp_short_frame_raises():
    client = _client()

    async def fake_send(_frame: bytes) -> bytes:
        return b"\x00\x01"

    client._send_receive_frame = fake_send
    with pytest.raises(FrameError, match="Short Modbus TCP"):
        await client._parse_adu_from_tcp_response(3, 0, count=1)


@pytest.mark.asyncio
async def test_parse_tcp_exception_is_modbus_error():
    client = _client()
    exception = _mbap_pdu(bytes([0x83, 0x02]))

    async def fake_send(_frame: bytes) -> bytes:
        return exception

    client._send_receive_frame = fake_send
    with pytest.raises(Exception):
        await client._parse_adu_from_tcp_response(3, 0, count=12)


@pytest.mark.asyncio
async def test_parse_tcp_holding_registers():
    client = _client()
    pdu = bytes([0x03, 4, 0x00, 0x0A, 0x00, 0x14])
    response = _mbap_pdu(pdu)

    async def fake_send(frame: bytes) -> bytes:
        assert frame[6] == 1
        return response

    client._send_receive_frame = fake_send
    values = await client._parse_adu_from_tcp_response(3, 0, count=2)
    assert values == [10, 20]


def test_connected_false_without_keeper():
    assert _client().connected is False
