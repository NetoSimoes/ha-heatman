# Overview

**Heatman** is a Home Assistant custom integration for heat pumps over Modbus.

| Fact | Value |
|------|-------|
| Type | Custom integration (not an add-on) |
| Domain | `heatman` |
| Path | [`custom_components/heatman/`](../custom_components/heatman/) |
| Integration type | `device` |
| IoT class | `local_polling` |
| Config | UI config flow |
| Min Home Assistant | `2025.2.0` ([`hacs.json`](../hacs.json)) |
| Python requirement | `aiofiles` (Modbus stack vendored as `pysolarman`) |
| License | MIT ([`license`](../license)) |

## What it does

1. Connects via **Modbus TCP** (default) or Modbus RTU (legacy Solarman TCP framing still available).
2. Loads a YAML **profile** from `heatpump_definitions/` that maps registers to entities.
3. Polls on a 5-second coordinator tick; each parameter has its own `update_interval`.
4. Exposes sensors and writable entities (switch, number, select, button, datetime, time).
5. Offers raw Modbus services for debugging.

## First profile

[`midea_mthermal_a.yaml`](../custom_components/heatman/heatpump_definitions/midea_mthermal_a.yaml) — Midea M-Thermal A Series / Solius OEM map. See [midea-mthermal.md](target/midea-mthermal.md).

## Not yet implemented

- Native `climate` and `water_heater` platforms (use number/select/switch for now)
- Brand autodetection

## Install

- Copy `custom_components/heatman/` into HA config, or install via HACS when available (`heatman.zip`).
- Add integration **Heatman** from the UI.

## Heritage

The polling engine descends from [ha-solarman](https://github.com/davidrapan/ha-solarman). Heatman is a separate integration: new domain, heat-pump profiles, no bundled solar inverter maps.
