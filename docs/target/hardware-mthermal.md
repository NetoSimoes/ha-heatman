# M-Thermal hardware

## RS-485 on the wired controller

Modbus RTU is exposed on the **wired controller** PCB ports **H1** and **H2**. The wired controller must be connected to the hydronic box or registers will not be accessible.

| Signal | Port |
|--------|------|
| BUS1 (A+) | H2 |
| BUS2 (B-) | H1 |

Confirmed by Planet Devices M-Thermal R32/R290 quick start guide.

## Serial settings

- Protocol: Modbus RTU slave
- Baud: **9600**, 8 data bits, no parity, 1 stop bit
- Default slave ID: **1** (hydronic main PCB rotary switch **S3** position **0**)

## Models

Outdoor: MHA-V4W–V16W (4–16 kW), D2N8-B / D2RN8-B variants. Hydronic: HB-A60/A100/A160/CGN8-B. OEM clones sharing the same controller/box hardware use the same map.

## TCP gateway

Typical setup: WaveShare RS485-to-Ethernet or EW11-class WiFi bridge.

1. Set gateway mode to **Modbus TCP ↔ Modbus RTU**.
2. Serial side: 9600 8N1.
3. TCP port: **502**.
4. Give the gateway a static IP or DHCP reservation.

In Heatman: transport `modbus_tcp`, port `502`, slave ID matching S3, profile `midea_mthermal_a.yaml`.

## Troubleshooting

| Symptom | Check |
|---------|-------|
| No Modbus data | Wired controller connected? H1/H2 polarity? S3 address? |
| H0 error | Outdoor ↔ hydronic communication (P/Q/E), power supply |
| E3–E9 / HA / Ed | Temperature sensor wiring on PCB |
| P0 / P1 | Low / high refrigerant pressure protections |

## References

- Planet Devices M-Thermal quick start (H1/H2, S3)
- Solius live HA Modbus config (register verification)
- Community / TapHome M-Thermal templates
