# ThunderCat6 Firmware Architecture

## Document Control
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-05-30 | - | Placeholder - awaiting datasheets |

---

## TODO: Required Information

- [ ] BR firmware/NVM programming guide
- [ ] KR configuration guide
- [ ] FX20 firmware SDK / programming guide
- [ ] PMG1-S3 EZ-PD Configuration Utility docs
- [ ] Backdoor controller selection (FTDI, MCU, etc.)

---

## Firmware Components

### BR (Barlow Ridge)
**TODO: From Intel documentation**
- Firmware type: **TODO**
- Configuration method: **TODO**
- Update procedure: **TODO**

### KR (Kite Ridge)
**TODO: From Intel documentation**
- Firmware type: **TODO**
- Configuration method: **TODO**

### FX20
**TODO: From Infineon documentation**
- Firmware type: **TODO**
- SDK: **TODO**
- I2C register map: **TODO**

### PD Controller (PMG1-S3)
**TODO: From Infineon documentation**
- Configuration tool: EZ-PD Configurator (confirmed)
- PDO configuration: **TODO**

---

## Control Interface

**TODO: Define after HW architecture is finalized**

- Host communication: **TODO**
- Command protocol: **TODO**
- Register definitions: **TODO**

---

## Next Steps

1. Obtain firmware/SDK documentation for each IC
2. Define control architecture (MCU vs FTDI vs direct)
3. Create register map based on datasheets
4. Develop firmware update procedures
5. Implement host API
