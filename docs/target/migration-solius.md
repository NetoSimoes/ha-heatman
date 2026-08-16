# Migrate from Solius core Modbus + templates

This guide maps a working Solius setup (`modbus:` hub + Jinja template switches/numbers) onto **Heatman**.

## Steps

1. Install [`custom_components/heatman/`](../../custom_components/heatman/).
2. Add integration **Heatman** with the same gateway host, port `502`, transport `modbus_tcp`, slave ID, profile `midea_mthermal_a.yaml`.
3. Confirm entities update (temps, mode, heating/DHW switches).
4. Point automations at the new entity IDs.
5. Remove the Solius entries from `modbus:` YAML and the template switches/numbers/select that only existed for Modbus RMW.
6. Restart HA.

Do **not** run both stacks writing the same registers at once.

## Entity mapping (conceptual)

| Old (examples) | Heatman profile entity name |
|----------------|-----------------------------|
| `switch.solius_heating` | Heating |
| `switch.solius_dhw` | DHW |
| `switch.solius_disinfection` | Disinfection |
| `switch.solius_silent` | Silent Mode |
| `switch.solius_eco` | Eco Mode |
| `select.solius_mode` | Mode |
| `number.solius_dhw_setpoint` | DHW Setpoint |
| `number.solius_heating_setpoint` | Heating Setpoint |
| `number.solius_room_setpoint` | Room Setpoint |
| `sensor.solius_tw_in` / `_out` | Inlet / Outlet Water Temperature |
| `sensor.solius_dhw_temp` | DHW Temperature |
| `sensor.solius_compressor_frequency` | Compressor Frequency |
| … | See [midea-mthermal.md](midea-mthermal.md) |

Exact `entity_id` values use your device name slug (default prefix from the config entry title).

## Keep as Home Assistant templates

These stay outside Heatman (depend on HA helpers or other integrations such as Deye):

- Calculated thermal power, estimated electrical power, COP (instant / lifetime / daily / monthly)
- Water delta-T, heating/DHW target error
- Solar surplus / solar-preheat condition sensors
- `integration` / `utility_meter` energy helpers

Re-point template sources at the new Heatman sensor entity IDs after cutover.

## Bit switches

Core Modbus has no `bit:` field — your templates used `bitwise_or` / `bitwise_and`. Heatman switches use native read-modify-write (`value.bit`), so those templates can be deleted.
