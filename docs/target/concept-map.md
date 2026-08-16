# Concept map

| Solar / old engine idea | Heatman |
|-------------------------|---------|
| Inverter | Heat pump (outdoor + hydronic) |
| Stick logger discovery | Manual host + Modbus TCP gateway |
| MPPT / phase / pack options | Slave ID + profile only |
| `inverter_definitions/` | `heatpump_definitions/` |
| PV / battery sensors | Flow/return, DHW, compressor, pressures |
| Domain `solarman` | Domain `heatman` |

Bitfield “power” register on M-Thermal (H:0) replaces a simple on/off inverter register: Heating and DHW are independent bits.
