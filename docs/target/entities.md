# Target entities

## Today (shipped)

M-Thermal profile uses existing platforms: switch, select, number, sensor, binary_sensor (connection). See [midea-mthermal.md](midea-mthermal.md).

## Future

### `climate`

Space heating circuit: current temp (Tw_out / T1), target (heating setpoint), HVAC mode (from Mode select), action from operating mode / compressor.

### `water_heater`

DHW: current tank temp (H:115), target (H:4), operation mode / boost.

Until then, use **Heating Setpoint**, **DHW Setpoint**, **Mode**, **Heating**, and **DHW** entities from the profile.
