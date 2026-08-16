"""Minimal Home Assistant stubs so Heatman modules import without Core."""

from __future__ import annotations

import re
import sys
import types
from enum import Enum


def _slugify(text: str, separator: str = "_") -> str:
    text = text.lower()
    text = re.sub(rf"[^a-z0-9{re.escape(separator)}]+", separator, text)
    return text.strip(separator)


def _format_mac(mac: str) -> str:
    hex_only = re.sub(r"[^0-9a-fA-F]", "", mac)
    if len(hex_only) == 12:
        return ":".join(hex_only[i : i + 2] for i in range(0, 12, 2)).lower()
    return mac.replace("-", ":").lower()


def _module(name: str) -> types.ModuleType:
    mod = types.ModuleType(name)
    sys.modules[name] = mod
    return mod


class _Platform(str, Enum):
    SENSOR = "sensor"
    BINARY_SENSOR = "binary_sensor"
    SWITCH = "switch"
    NUMBER = "number"
    SELECT = "select"
    BUTTON = "button"
    DATETIME = "datetime"
    TIME = "time"


class _AbortFlow(Exception):
    def __init__(self, reason: str, *args, **kwargs):
        super().__init__(reason)
        self.reason = reason


class _ConfigFlow:
    def __init__(self, *args, **kwargs):
        self.hass = None

    def __init_subclass__(cls, domain: str | None = None, **kwargs):
        cls.domain = domain

    def _async_current_entries(self, include_ignore: bool = True):
        return []

    def add_suggested_values_to_schema(self, schema, suggested):
        return schema

    def async_show_form(self, **kwargs):
        return kwargs

    def async_create_entry(self, **kwargs):
        return kwargs


class _OptionsFlow:
    pass


class _ConfigEntry:
    def __init__(self, **kwargs):
        self.title = kwargs.get("title", "")
        self.options = kwargs.get("options", {})
        self.data = kwargs.get("data", {})
        self.entry_id = kwargs.get("entry_id", "entry")
        self.version = kwargs.get("version", 1)
        self.minor_version = kwargs.get("minor_version", 0)


class _SelectSelectorConfig:
    def __init__(self, **kwargs):
        self.options = kwargs.get("options", [])


class _SelectSelector:
    def __init__(self, config):
        self.config = config


class _Coordinator:
    __class_getitem__ = classmethod(lambda cls, _item: cls)

    def __init__(self, *args, **kwargs):
        self.hass = args[0] if args else kwargs.get("hass")
        self.logger = args[1] if len(args) > 1 else kwargs.get("logger")
        self.config_entry = kwargs.get("config_entry")
        self.name = kwargs.get("name", "")
        self.data = {}
        self.last_update_success = True
        self._update_interval = kwargs.get("update_interval")
        self._update_interval_seconds = getattr(self._update_interval, "total_seconds", lambda: 5)() if self._update_interval else 5

    async def async_config_entry_first_refresh(self):
        return None

    async def async_shutdown(self):
        return None

    def _async_refresh_finished(self):
        return None

    @property
    def update_interval(self):
        return self._update_interval

    @update_interval.setter
    def update_interval(self, value):
        self._update_interval = value
        self._update_interval_seconds = getattr(value, "total_seconds", lambda: 5)() if value else 5


def install() -> None:
    if "homeassistant.helpers.device_registry" in sys.modules:
        return

    ha = _module("homeassistant")
    ha.const = _module("homeassistant.const")
    ha.const.CONF_NAME = "name"
    ha.const.CONF_FRIENDLY_NAME = "friendly_name"
    ha.const.STATE_UNKNOWN = "unknown"
    ha.const.Platform = _Platform
    ha.const.EntityCategory = types.SimpleNamespace(CONFIG="config", DIAGNOSTIC="diagnostic")

    ha.core = _module("homeassistant.core")
    ha.core.HomeAssistant = object
    ha.core.callback = lambda f: f
    ha.core.split_entity_id = lambda entity_id: entity_id.split(".", 1)
    ha.core.ServiceCall = object
    ha.core.SupportsResponse = types.SimpleNamespace(OPTIONAL="optional", ONLY="only", NONE="none")

    ha.util = _module("homeassistant.util")
    ha.util.slugify = _slugify

    ha.helpers = _module("homeassistant.helpers")
    ha.helpers.typing = _module("homeassistant.helpers.typing")
    ha.helpers.typing.ConfigType = dict
    ha.helpers.typing.StateType = object
    ha.helpers.typing.UNDEFINED = object()
    ha.helpers.typing.UndefinedType = type(None)

    ha.helpers.device_registry = _module("homeassistant.helpers.device_registry")
    ha.helpers.device_registry.CONNECTION_NETWORK_MAC = "mac"
    ha.helpers.device_registry.DeviceInfo = dict
    ha.helpers.device_registry.DeviceEntry = object
    ha.helpers.device_registry.format_mac = _format_mac
    ha.helpers.device_registry.async_get = lambda hass: None

    ha.helpers.entity_registry = _module("homeassistant.helpers.entity_registry")
    ha.helpers.entity_registry.RegistryEntry = object
    ha.helpers.entity_registry.async_get = lambda hass: None
    ha.helpers.entity_registry.async_migrate_entries = lambda *a, **k: None

    ha.helpers.config_validation = _module("homeassistant.helpers.config_validation")
    ha.helpers.config_validation.port = int
    ha.helpers.config_validation.positive_int = int
    ha.helpers.config_validation.empty_config_schema = lambda domain: {}
    ha.helpers.config_validation.ensure_list = lambda value: value if isinstance(value, list) else [value]

    ha.helpers.selector = _module("homeassistant.helpers.selector")
    ha.helpers.selector.SelectSelector = _SelectSelector
    ha.helpers.selector.SelectSelectorConfig = _SelectSelectorConfig

    ha.helpers.update_coordinator = _module("homeassistant.helpers.update_coordinator")
    ha.helpers.update_coordinator.DataUpdateCoordinator = _Coordinator
    ha.helpers.update_coordinator.UpdateFailed = Exception
    ha.helpers.update_coordinator.CoordinatorEntity = type(
        "CoordinatorEntity",
        (),
        {"__class_getitem__": classmethod(lambda cls, _item: cls), "__init__": lambda self, coordinator: None},
    )

    ha.helpers.entity = _module("homeassistant.helpers.entity")
    ha.helpers.entity.EntityDescription = dict

    ha.exceptions = _module("homeassistant.exceptions")
    ha.exceptions.ServiceValidationError = type("ServiceValidationError", (Exception,), {})

    ha.data_entry_flow = _module("homeassistant.data_entry_flow")
    ha.data_entry_flow.section = lambda schema, options=None: schema
    ha.data_entry_flow.AbortFlow = _AbortFlow

    ha.config_entries = _module("homeassistant.config_entries")
    ha.config_entries.ConfigEntry = _ConfigEntry
    ha.config_entries.ConfigFlow = _ConfigFlow
    ha.config_entries.ConfigFlowResult = dict
    ha.config_entries.OptionsFlow = _OptionsFlow

    ha.loader = _module("homeassistant.loader")
    ha.loader.async_get_integration = None
    ha.loader.IntegrationNotFound = type("IntegrationNotFound", (Exception,), {})
