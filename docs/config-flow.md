# Config flow

UI-only. Options stored on the config entry. Handler: [`config_flow.py`](../custom_components/heatman/config_flow.py).

## Fields

| Field | Key | Default |
|-------|-----|---------|
| Device name | `name` | `Heat Pump` |
| Host | `host` | — |
| Port | `port` | `502` |
| Transport | `transport` | `modbus_tcp` |
| Profile | `lookup_file` | `midea_mthermal_a.yaml` |
| Modifier | `mod` | `0` |
| Modbus slave ID | `mb_slave_id` | `1` |

No DHCP or UDP stick discovery. Manual host entry only.

Profiles are listed from `heatpump_definitions/` and `heatpump_definitions/custom/`.
