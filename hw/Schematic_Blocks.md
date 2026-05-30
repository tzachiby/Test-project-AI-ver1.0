# ThunderCat6 Schematic Blocks

## Document Control
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-05-30 | - | Placeholder - awaiting datasheets |

---

## TODO: Required Datasheets

- [ ] BR (Barlow Ridge) - pinout, interfaces
- [ ] KR (Kite Ridge) - pinout, interfaces
- [ ] FX20 - pinout, I2C address, control interface
- [ ] PMG1-S3 - pinout, configuration
- [ ] RTD2198 - pinout, I2C/AUX interface
- [ ] FTDI controller - if used for backdoor

---

## Block Diagram (Conceptual - From Requirements)

```
UFP (Type-C) ──► [Signal Routing] ──► BR (TBT4)
                      │                   │
                      │                   ├──► M.2 SSD (PCIe)
                      │                   ├──► MST Hub (DP)
                      │                   └──► USB3
                      │
                      ├──► KR (USB4)
                      │
                      └──► FX20 (USB Traffic Gen)
                                │
                                └──► DFP Ports
```

---

## Interface Details

### BR Interfaces
**TODO: From BR datasheet**
- USB4/TBT port: **TODO**
- PCIe lanes: **TODO**
- DP output: **TODO**
- Control interface: **TODO**

### KR Interfaces
**TODO: From KR datasheet**
- USB4 port: **TODO**
- Control interface: **TODO**

### FX20 Interfaces
**TODO: From FX20 datasheet**
- USB3.2 port: **TODO**
- Control interface: **TODO**
- I2C address: **TODO**

### PD Controller Interfaces
**TODO: From PMG1-S3 datasheet**
- CC lines: **TODO**
- I2C address: **TODO**
- VBUS control: **TODO**

---

## Control Architecture

**TODO: Define after obtaining datasheets**

- Backdoor interface: **TODO**
- I2C bus topology: **TODO**
- GPIO assignments: **TODO**
- Mode selection mechanism: **TODO**

---

## Next Steps

1. Obtain IC datasheets
2. Define control interface (FTDI, MCU, etc.)
3. Create detailed pin assignments
4. Design power distribution
5. Create schematic
