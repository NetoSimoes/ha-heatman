# Heatman documentation

**Heatman** (`domain: heatman`) is a Home Assistant custom integration for heat pumps over Modbus.

## Start here

| Document | Description |
|----------|-------------|
| [Overview](overview.md) | What Heatman is, install, license |
| [Architecture](architecture.md) | Modules and poll loop |
| [Modbus](modbus.md) | Transports, function codes, batching |
| [Profile schema](profile-schema.md) | YAML register-map format |
| [Config flow](config-flow.md) | Setup fields |
| [Entities](entities.md) | Platforms |
| [Services](services.md) | Raw Modbus services |
| [Development](development.md) | Layout and CI |
| [Glossary](glossary.md) | Terms |

## M-Thermal / Solius

| Document | Description |
|----------|-------------|
| [Register map](target/midea-mthermal.md) | Solius-verified holding registers |
| [Hardware](target/hardware-mthermal.md) | H1/H2, S3, WaveShare/EW11 |
| [Migration](target/migration-solius.md) | Leave core `modbus:` + Jinja for Heatman |
| [Vision](target/vision.md) | Product direction |
| [Target entities](target/entities.md) | Future climate / water_heater |
| [Conversion](target/conversion.md) | Engine heritage checklist (mostly done) |
