# Profile YAML schema

Profiles live in [`custom_components/heatman/heatpump_definitions/`](../custom_components/heatman/heatpump_definitions/). Custom files go in `heatpump_definitions/custom/` (HACS persistent directory).

Parser: [`ParameterParser`](../custom_components/heatman/parser.py).

## Structure

```yaml
info:
  manufacturer: Midea
  model: M-Thermal A Series

default:
  update_interval: 30
  digits: 1
  code: 0x03

parameters:
  - group: Control
    items:
      - name: "Heating"
        platform: switch
        rule: 1
        registers: [0]
        value:
          bit: 1
```

## Parsing rules

| Rule | Type |
|------|------|
| 1, 3 | Unsigned |
| 2, 4 | Signed |
| 5 | ASCII |
| 6 | Hex bits |
| 7 | Version |
| 8 | Datetime |
| 9 | Time |
| 10 | Raw list |

Multi-register unsigned values pack the **first listed register as the low word**.

## Platforms

`sensor` (default), `binary_sensor`, `switch`, `number`, `select`, `button`, `datetime`, `time`.

Bit switches use `value.bit` with read-modify-write ([`HeatmanSwitchEntity`](../custom_components/heatman/switch.py)).

Reference profile: [`midea_mthermal_a.yaml`](../custom_components/heatman/heatpump_definitions/midea_mthermal_a.yaml).
