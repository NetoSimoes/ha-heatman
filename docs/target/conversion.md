# Conversion checklist status

Most of the Solarman → Heatman conversion is **done** in this repository.

| Step | Status |
|------|--------|
| Domain `heatman` | Done |
| Folder `custom_components/heatman/` | Done |
| HACS / manifest Heatman | Done |
| `heatpump_definitions/` + M-Thermal profile | Done |
| Defaults 502 / `modbus_tcp` | Done |
| Drop solar YAMLs, stick HTTP, battery helpers, discovery | Done |
| Config flow without MPPT/battery options | Done |
| Docs for Solius migration | Done |
| `climate` / `water_heater` platforms | Deferred |
| Tests | Deferred |

Keep the vendored `pysolarman` package name as an internal Modbus client for now.
