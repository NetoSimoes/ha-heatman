from re import compile
from datetime import timedelta
from aiohttp import BasicAuth, FormData

DOMAIN = "heatman"

IP_BROADCAST = "<broadcast>"
IP_ANY = "0.0.0.0"

PORT_ANY = 0

# Legacy Solarman stick discovery constants (unused by Heatman setup)
DISCOVERY_PORT = 48899
DISCOVERY_TIMEOUT = .5
DISCOVERY_MESSAGE = ["WIFIKIT-214028-READ".encode(), "HF-A11ASSISTHREAD".encode()]
DISCOVERY_INTERVAL = timedelta(minutes = 15)
DISCOVERY_CACHE = timedelta(seconds = 10)

COMPONENTS_DIRECTORY = "custom_components"

LOOKUP_DIRECTORY = "heatpump_definitions"
LOOKUP_DIRECTORY_PATH = f"{COMPONENTS_DIRECTORY}/{DOMAIN}/{LOOKUP_DIRECTORY}/"
LOOKUP_CUSTOM_DIRECTORY_PATH = f"{COMPONENTS_DIRECTORY}/{DOMAIN}/{LOOKUP_DIRECTORY}/custom/"

CONF_HOST = "host"
CONF_PORT = "port"
CONF_TRANSPORT = "transport"
CONF_LOOKUP_FILE = "lookup_file"
CONF_ADDITIONAL_OPTIONS = "additional_options"
CONF_MOD = "mod"
CONF_MB_SLAVE_ID = "mb_slave_id"

OLD_ = { "name": "name", "serial": "inverter_serial", "sn": "serial", "sn": "sn", CONF_HOST: "inverter_host", CONF_PORT: "inverter_port" }

LOGGER_AUTH = BasicAuth("admin", "admin")
LOGGER_SET = "hide_set_edit.html"
LOGGER_CMD = "do_cmd.html"
LOGGER_SUCCESS = "success.html"
LOGGER_RESTART = "restart.html"
LOGGER_RESTART_DATA = FormData({"HF_PROCESS_CMD": "RESTART"})
LOGGER_REGEX = {"setting_protocol": compile("var net_setting_pro.?=.?\"(.*)\";"), "setting_cs": compile("var net_setting_cs.?=.?\"(.*)\";"), "setting_port": compile("var net_setting_port.?=.?\"(.*)\";"), "setting_ip": compile("var net_setting_ip.?=.?\"(.*)\";"), "setting_timeout": compile("var net_setting_to.?=.?\"(.*)\";"), "mode": compile("var yz_tmode.?=.?\"(.*)\";"), "server": compile("var server_[a|b].?=.?\"(.*)\";"), "ap": compile("var apsta_mode.?=.?\"(.*)\";")}

SUGGESTED_VALUE = "suggested_value"
UPDATE_INTERVAL = "update_interval"
IS_SINGLE_CODE = "is_single_code"
REGISTERS_CODE = "registers_code"
REGISTERS_MIN_SPAN = "registers_min_span"
REGISTERS_MAX_SIZE = "registers_max_size"
DIGITS = "digits"

DEFAULT_ = {
    "name": "Heat Pump",
    CONF_HOST: "",
    CONF_PORT: 502,
    CONF_TRANSPORT: "modbus_tcp",
    CONF_MB_SLAVE_ID: 1,
    CONF_LOOKUP_FILE: "midea_mthermal_a.yaml",
    CONF_MOD: 0,
    UPDATE_INTERVAL: 60,
    IS_SINGLE_CODE: False,
    REGISTERS_CODE: 0x03,
    REGISTERS_MIN_SPAN: 25,
    REGISTERS_MAX_SIZE: 125,
    DIGITS: 6
}

PROFILE_REDIRECT = {}

PARAM_ = { CONF_MOD: CONF_MOD }

TIMINGS_INTERVAL = 5
TIMINGS_INTERVAL_SCALE = 1
TIMINGS_UPDATE_INTERVAL = timedelta(seconds = TIMINGS_INTERVAL * TIMINGS_INTERVAL_SCALE)

REQUEST_UPDATE_INTERVAL = UPDATE_INTERVAL
REQUEST_MIN_SPAN = "min_span"
REQUEST_MAX_SIZE = "max_size"
REQUEST_CODE = "code"
REQUEST_CODE_ALT = "mb_functioncode"
REQUEST_START = "start"
REQUEST_END = "end"
REQUEST_COUNT = "count"

SERVICES_PARAM_DEVICE = "device"
SERVICES_PARAM_ADDRESS = "address"
SERVICES_PARAM_COUNT = "count"
SERVICES_PARAM_QUANTITY = "quantity"
SERVICES_PARAM_VALUE = "value"
SERVICES_PARAM_VALUES = "values"

SERVICE_READ_HOLDING_REGISTERS = "read_holding_registers"
SERVICE_READ_INPUT_REGISTERS = "read_input_registers"
SERVICE_WRITE_SINGLE_REGISTER = "write_single_register"
SERVICE_WRITE_MULTIPLE_REGISTERS = "write_multiple_registers"

SERVICES_PARAM_REGISTER = "register"
SERVICES_PARAM_QUANTITY = "quantity"
DEPRECATION_SERVICE_WRITE_SINGLE_REGISTER = "write_holding_register"
DEPRECATION_SERVICE_WRITE_MULTIPLE_REGISTERS = "write_multiple_holding_registers"

DATETIME_FORMAT = "%y/%m/%d %H:%M:%S"
TIME_FORMAT = "%H:%M"
