# Profile template

Prefer the real profile: [`midea_mthermal_a.yaml`](../../custom_components/heatman/heatpump_definitions/midea_mthermal_a.yaml).

For a new brand, copy that file into `heatpump_definitions/custom/`, change `info`, and replace registers using [profile schema](../profile-schema.md). Validate with `heatman.read_holding_registers` before enabling writes.
