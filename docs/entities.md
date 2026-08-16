# Entities

Base classes in [`entity.py`](../custom_components/heatman/entity.py): `HeatmanEntity`, `HeatmanWritableEntity`.

## Platforms

| Platform | Writable | Notes |
|----------|----------|-------|
| sensor | No | Plus diagnostic update-interval sensor |
| binary_sensor | No | Plus connection diagnostic |
| switch | Yes | Bitfield RMW supported |
| number | Yes | Setpoints |
| select | Yes | Mode enums |
| button | Yes | Pulse writes |
| datetime / time | Yes | If a profile defines them |

There is no `climate` or `water_heater` platform yet — use number/select/switch for M-Thermal control. See [target entities](target/entities.md).
