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

## Tests

`pytest` from the repo root. Optional extras: `pip install -e ".[test]"`.

CI runs hassfest, HACS validation, and pytest.

Release zip name is derived from the repo name suffix (`heatman` from `ha-heatman`) in [`assets.yaml`](../.github/workflows/assets.yaml).

## Custom profiles

`custom_components/heatman/heatpump_definitions/custom/`

## Adding a profile

1. Author YAML under `heatpump_definitions/` using [profile schema](profile-schema.md).
2. Restart HA / reload Heatman; select the file in config flow.
3. Validate with [Modbus services](services.md).
