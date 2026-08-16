# Heatman

Home Assistant custom integration for **heat pumps over Modbus**.

Domain: `heatman`. First supported map: **Midea M-Thermal A Series** (and OEM clones such as Solius), verified against a live Modbus TCP setup.

Built on the YAML-driven Modbus engine from [ha-solarman](https://github.com/davidrapan/ha-solarman) (MIT), rebranded and retargeted for heat pumps.

## Features

- Local Modbus TCP / RTU polling (default port **502**, transport **modbus_tcp**)
- Declarative register profiles under `heatpump_definitions/`
- Native switches (including bitfield RMW), selects, numbers, and sensors
- Raw Modbus read/write services for debugging

## Documentation

- [Documentation index](docs/README.md)
- [M-Thermal / Solius register map](docs/target/midea-mthermal.md)
- [Hardware (H1/H2, S3, gateway)](docs/target/hardware-mthermal.md)
- [Migrate from core `modbus:` + templates](docs/target/migration-solius.md)

## Installation

### Manual

1. Copy `custom_components/heatman/` into your Home Assistant `custom_components/` directory.
2. Restart Home Assistant.
3. Settings → Devices & services → Add integration → **Heatman**.

### HACS

Add this repository as a custom integration repository when published; package name is **Heatman** (`heatman.zip`).

## Configuration

UI config flow only.

| Field | Default | Notes |
|-------|---------|-------|
| Name | `Heat Pump` | Entity prefix |
| Host | — | Gateway or device IP |
| Port | `502` | Modbus TCP |
| Transport | `modbus_tcp` | Or `modbus_rtu` / legacy `tcp` |
| Profile | `midea_mthermal_a.yaml` | From `heatpump_definitions/` |
| Modbus slave ID | `1` | Hydronic PCB S3 position 0 → 1 |

## Attribution

- Modbus engine based on [ha-solarman](https://github.com/davidrapan/ha-solarman) by David Rapan and contributors
- M-Thermal register map verified on Solius OEM hardware; community / TapHome lineage
- License: [MIT](license)
