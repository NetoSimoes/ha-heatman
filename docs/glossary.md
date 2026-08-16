# Glossary

| Term | Meaning |
|------|---------|
| **Domain** | `heatman` |
| **Profile** | YAML under `heatpump_definitions/` mapping registers to entities |
| **Coordinator** | Polls every 5 seconds |
| **ParameterParser** | Schedules reads and decodes values |
| **Transport** | `modbus_tcp` (default), `modbus_rtu`, or legacy Solarman `tcp` |
| **Slave ID** | Modbus unit ID (`mb_slave_id`) |
| **Holding / input** | FC 3 / FC 4 register spaces |
| **Bit switch** | RMW of one bit in a holding register (`value.bit`) |
| **M-Thermal** | Midea split heat pump + hydronic box family |
| **Solius** | OEM using the same Modbus map (verified source for the first profile) |
| **DHW** | Domestic hot water |
| **COP** | Coefficient of performance (usually computed in HA templates) |
