from __future__ import annotations

from unittest.mock import patch

from heatman.config_flow import remove_defaults, validate_connection
from heatman.const import (
    CONF_ADDITIONAL_OPTIONS,
    CONF_HOST,
    CONF_LOOKUP_FILE,
    CONF_MB_SLAVE_ID,
    CONF_PORT,
    CONF_TRANSPORT,
    DEFAULT_,
    DOMAIN,
)


def test_remove_defaults_strips_matching_values():
    user_input = {
        CONF_HOST: "10.0.0.5",
        CONF_PORT: DEFAULT_[CONF_PORT],
        CONF_TRANSPORT: DEFAULT_[CONF_TRANSPORT],
        CONF_LOOKUP_FILE: DEFAULT_[CONF_LOOKUP_FILE],
        CONF_ADDITIONAL_OPTIONS: {CONF_MB_SLAVE_ID: DEFAULT_[CONF_MB_SLAVE_ID], "mod": 1},
    }
    cleaned = remove_defaults(dict(user_input))
    assert CONF_PORT not in cleaned
    assert CONF_TRANSPORT not in cleaned
    assert cleaned[CONF_HOST] == "10.0.0.5"
    assert cleaned[CONF_ADDITIONAL_OPTIONS] == {"mod": 1}


def test_remove_defaults_drops_empty_additional_options():
    user_input = {
        CONF_HOST: "10.0.0.5",
        CONF_ADDITIONAL_OPTIONS: {CONF_MB_SLAVE_ID: DEFAULT_[CONF_MB_SLAVE_ID]},
    }
    cleaned = remove_defaults(user_input)
    assert CONF_ADDITIONAL_OPTIONS not in cleaned


def test_validate_connection_localhost():
    assert validate_connection({CONF_HOST: "127.0.0.1", CONF_PORT: 502}) is None


def test_validate_connection_cannot_connect():
    with patch("heatman.config_flow.getaddrinfo", side_effect=__import__("socket").gaierror):
        assert validate_connection({CONF_HOST: "no.such.host", CONF_PORT: 502}) == {"base": "cannot_connect"}


def test_domain_and_defaults():
    assert DOMAIN == "heatman"
    assert DEFAULT_[CONF_TRANSPORT] == "modbus_tcp"
    assert DEFAULT_[CONF_PORT] == 502
    assert DEFAULT_[CONF_LOOKUP_FILE] == "midea_mthermal_a.yaml"
