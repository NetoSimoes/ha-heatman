# Development

```
ha-heatman/
├── custom_components/heatman/
│   ├── brand/                  # HACS / HA icon.png
│   ├── heatpump_definitions/   # Device YAML profiles
│   ├── pysolarman/             # Vendored Modbus client
│   ├── translations/
│   └── *.py
├── docs/
├── tools/                      # Legacy Solarman stick helpers
├── hacs.json
├── license
└── readme.md
```

## CI

[`.github/workflows/ha.yaml`](../.github/workflows/ha.yaml) — hassfest + HACS validation.

Release zip name is derived from the repo name suffix (`heatman` from `ha-heatman`) in [`assets.yaml`](../.github/workflows/assets.yaml).

## Custom profiles

`custom_components/heatman/heatpump_definitions/custom/`

## Adding a profile

1. Author YAML under `heatpump_definitions/` using [profile schema](profile-schema.md).
2. Restart HA / reload Heatman; select the file in config flow.
3. Validate with [Modbus services](services.md).
