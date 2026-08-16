from __future__ import annotations

from logging import getLogger

from homeassistant.core import HomeAssistant
from homeassistant.const import EntityCategory
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import RestoreSensor, SensorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import *
from .common import *
from .services import *
from .entity import HeatmanEntity, Coordinator

_LOGGER = getLogger(__name__)

_PLATFORM = get_current_file_name(__name__)

def _create_entity(coordinator, description):
    if "persistent" in description:
        return HeatmanPersistentSensor(coordinator, description)

    if "restore" in description or "ensure_increasing" in description:
        return HeatmanRestoreSensor(coordinator, description)

    if "via_device" in description:
        return HeatmanNestedSensor(coordinator, description)

    return HeatmanSensor(coordinator, description)

async def async_setup_entry(_: HomeAssistant, config_entry: ConfigEntry[Coordinator], async_add_entities: AddEntitiesCallback) -> bool:
    _LOGGER.debug(f"async_setup_entry: {config_entry.options}")

    async_add_entities([HeatmanIntervalSensor(config_entry.runtime_data)] + [_create_entity(config_entry.runtime_data, d).init() for d in config_entry.runtime_data.device.profile.parser.get_entity_descriptions(_PLATFORM)])

    return True

async def async_unload_entry(_: HomeAssistant, config_entry: ConfigEntry[Coordinator]) -> bool:
    _LOGGER.debug(f"async_unload_entry: {config_entry.options}")

    return True

class HeatmanSensorEntity(HeatmanEntity, SensorEntity):
    def __init__(self, coordinator, sensor):
        super().__init__(coordinator, sensor)
        if "state_class" in sensor and (state_class := sensor["state_class"]):
            self._attr_state_class = state_class

class HeatmanIntervalSensor(HeatmanSensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator, {"key": "update_interval_sensor", "name": "Update Interval"})
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_native_unit_of_measurement = "s"
        self._attr_state_class = "measurement"
        self._attr_device_class = "duration"
        self._attr_icon = "mdi:update"
        self._attr_native_value = 0

    @property
    def available(self) -> bool:
        return self._attr_native_value is not None

    def update(self):
        self.set_state(self.coordinator.device.state.updated_interval.total_seconds())

class HeatmanSensor(HeatmanSensorEntity):
    def __init__(self, coordinator, sensor):
        super().__init__(coordinator, sensor)
        self._sensor_ensure_increasing = "ensure_increasing" in sensor

class HeatmanNestedSensor(HeatmanSensorEntity):
    def __init__(self, coordinator, sensor):
        super().__init__(coordinator, sensor)
        parent_device_info = self.coordinator.device.info.get(self.coordinator.config_entry.entry_id)
        device_serial_number, _ = self.coordinator.data[slugify(sensor["group"], "serial", "number", "sensor")]
        if not device_serial_number in self.coordinator.device.info:
            self.coordinator.device.info[device_serial_number] = build_device_info(None, str(device_serial_number), None, None, None, parent_device_info["name"])
            self.coordinator.device.info[device_serial_number]["via_device"] = (DOMAIN, parent_device_info.get("serial_number", self.coordinator.config_entry.entry_id))
            self.coordinator.device.info[device_serial_number]["manufacturer"] = parent_device_info["manufacturer"]
            self.coordinator.device.info[device_serial_number]["model"] = None
        self._attr_device_info = self.coordinator.device.info[device_serial_number]
        self._attr_name.replace(f"{sensor["group"]} ", '')

class HeatmanRestoreSensor(HeatmanSensor, RestoreSensor):
    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if last_sensor_data := await self.async_get_last_sensor_data():
            self._attr_native_value = last_sensor_data.native_value

    def set_state(self, state, value = None) -> bool:
        if self._sensor_ensure_increasing and self._attr_native_value is not None and state is not None and self._attr_native_value > state > 0:
            return False
        return super().set_state(state, value)

class HeatmanPersistentSensor(HeatmanRestoreSensor):
    @property
    def available(self) -> bool:
        return True
