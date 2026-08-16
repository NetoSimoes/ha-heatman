# Midea M-Thermal A Series register map

Profile: [`midea_mthermal_a.yaml`](../../custom_components/heatman/heatpump_definitions/midea_mthermal_a.yaml)

Verified against a live **Solius** OEM installation using Home Assistant core Modbus + templates. Same map applies to Midea M-Thermal A Series Split (R32) and compatible OEM clones (Hyundai, Concept, Hajdu, Immergas, Clivet Swan) when using the same wired controller and hydronic box.

Community-sourced holding registers — not an official Midea public Modbus manual.

## Controls

| Reg | Entity | Encoding |
|-----|--------|----------|
| 0 | Heating | Bit 1 (mask 2), RMW |
| 0 | DHW | Bit 2 (mask 4), RMW |
| 5 | Disinfection | Bit 4 (mask 16) |
| 5 | Silent Mode | Bit 6 (mask 64) |
| 5 | Eco Mode | Bit 10 (mask 1024) |
| 1 | Mode | 1=auto, 2=cool, 3=heat |
| 3 | Room setpoint | Int16 °C, 16–30 |
| 4 | DHW setpoint | Int16 °C, 40–60 |
| 7 | Forced water heating | 1/0 |
| 8 | Forced TBH | 1/0 |
| 9 | Forced IBH1 | 1/0 |
| 11 | Heating setpoint | Int16 °C, 17–65 |
| 6 | Curve selection | UInt16 |
| 10 | Smart Grid max setpoint | Int16 °C |

## Temperatures (Int16 °C)

104 Tw_in, 105 Tw_out, 110 T1 calculated, 107 outdoor T4, 115 DHW T5, 106 T3, 108 Tp discharge, 109 Th suction, 112 T2 liquid, 113 T2B gas, 136 weather-compensated target.

## Compressor / hydraulics

| Reg | Entity | Scale / unit |
|-----|--------|--------------|
| 100 | Compressor frequency | Hz |
| 102 | Fan speed | rpm |
| 122 | Compressor hours | h |
| 132 | Target frequency | Hz |
| 138 | Water flow | ×0.01 m³/h |
| 140 | Capacity | ×0.01 kW |

## Electrical / pressure

116/117 high/low pressure kPa; 118/119 ODU current/voltage; 133 DC bus current ×0.1 A; 134 DC bus voltage ×10 V; 250–252 IBH1/IBH2/TBH power kW.

## Status / energy

| Reg | Entity | Notes |
|-----|--------|-------|
| 101 | Operating mode | 0 Off, 2 Cool, 3 Heat, 5 DHW |
| 124 | Fault code | |
| 128 | Bit status 1 | |
| 129 | Load output | % |
| 130 | Firmware IDU | |
| 190 | Sub model | 3 R290-A, 4 R290-N, 9 R290-M |
| 143–144 | Electricity | uint32, ×0.01 kWh |
| 145–146 | Heat energy | uint32 kWh |

### Energy word order

Heatman packs the **first** register in the YAML list as the **low** word. Core HA `uint32` at address 143 is often high-word-first. If kWh totals disagree with your previous sensors, swap to `registers: [144, 143]` / `[146, 145]` in the profile.
