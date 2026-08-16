# Modbus

Client lives in [`pysolarman/`](../custom_components/heatman/pysolarman/) (class name `Solarman` — legacy package name).

## Transports

| Transport | Protocol | Typical port | Heatman use |
|-----------|----------|--------------|-------------|
| `modbus_tcp` | Standard Modbus TCP | **502** | **Default** — WaveShare / EW11 gateways |
| `modbus_rtu` | Modbus RTU ADU | varies | Direct RS485 bridges |
| `tcp` | Solarman proprietary framing | 8899 | Legacy only |

## Function codes

| Code | Use |
|------|-----|
| 3 | Read holding registers (profile default) |
| 4 | Read input registers |
| 6 | Write single register |
| 16 | Write multiple registers |

See [Services](services.md).

## Batching

| Setting | Default | M-Thermal profile |
|---------|---------|-------------------|
| `min_span` | 25 | **1** (do not fill unmapped holes) |
| `max_size` | 125 | **20** |
| `code` | 0x03 | 0x03 |

## Slave ID

`mb_slave_id` (default 1). On M-Thermal hydronic boxes, S3 position 0 → slave 1.
