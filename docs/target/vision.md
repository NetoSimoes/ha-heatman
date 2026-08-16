# Heatman vision

**Heatman** polls a heat pump over Modbus (TCP or RTU) and exposes heating, DHW, and diagnostics in Home Assistant.

## Primary target

**Midea M-Thermal A Series** (and OEM clones such as Solius) via RS-485 / Modbus TCP gateway.

- Local only (`local_polling`)
- Default transport `modbus_tcp` port 502
- Profile-driven entities today; future `climate` + `water_heater` platforms

## Connectivity priority

1. `modbus_tcp` (WaveShare / EW11) — recommended
2. `modbus_rtu`
3. Legacy Solarman `tcp` framing — only if required

## Reused engine

YAML profiles, coordinator scheduling, writable entities, and Modbus services come from the ha-solarman-derived stack (vendored as `pysolarman`).

## Next product steps

1. Native `climate` (heating circuit) and `water_heater` (DHW)
2. Additional brand profiles as maps are verified
3. Optional computed sensors (COP) inside the integration
