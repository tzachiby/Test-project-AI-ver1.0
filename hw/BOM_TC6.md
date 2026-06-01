# ThunderCat6 Bill of Materials (BOM)

## Document Control
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.2 | 2026-06-01 | - | Updated with KR/BR/TR datasheet specs |

---

## Datasheet Sources
- ✅ Kite Ridge 0.76 (March 2026)
- ✅ Barlow Ridge Accessory Training v1.2
- ✅ Tornado Ridge 0.5 Draft (July 2025)
- [ ] FX20 datasheet - Still needed from Infineon
- [ ] PMG1-S3 datasheet - Available from Infineon
- [ ] RTD2198 (MST Hub) datasheet - Still needed from Realtek

---

## Main Controllers

| Component | Version | Qty FV | Unit Cost | Notes |
|-----------|---------|--------|-----------|-------|
| BR (Barlow Ridge) | v1.2 | 1 | $20.00 | TBT4 Controller, 4-Port Hub |
| KR (Kite Ridge) | 0.76 | 1 | $10.00 | USB4 Hub Controller |
| TR (Tornado Ridge) | 0.5 | Optional | TBD | Based on KR, PCIe Mini Dock |
| FX20 | **TODO** | 1 | $60.00 | USB Traffic Generator |
| MST Realtek | RTD2198 | 4 | $20.00 | DP Sink Hub |
| PD Controller | PMG1-S3 | 2 | $2.34 | USB-PD |
| **Total FV** | | | **$493.43** | From TC6 Requirements |

---

## Power Requirements (From Datasheets)

### KR Power Rails
| Rail | Voltage | Tolerance | Max Current | Notes |
|------|---------|-----------|-------------|-------|
| VCC1P8_SX | 1.8V | 1.71-1.89V | 200mA | Main supply |
| VCC1P8_SX_IO | 1.8V | - | 100mA | I/O supply |
| VCC1P2 | 1.2V | 1.14-1.26V | 1250mA | Core logic |
| VCC0P8 | 0.8V | 0.7-0.9V | 4A | Adjustable via SVR_CNTL |

### BR SVR Requirements
| SVR | Output | Steps | Max Current | Inductor | Cout |
|-----|--------|-------|-------------|----------|------|
| 0.75V SVR | 0.67-0.924V | 256 (1mV) | 3A | 0.4µH ±20% | 6×22µF |
| 1.2V ASVR | 1.07-1.47V | 256 (1.6mV) | 1A | 0.6µH ±20% | 4×22µF |

### TR Power Rails
| Rail | Voltage | Source |
|------|---------|--------|
| VCC1P8_SX | 1.8V | External regulator |
| VCC1P2 | 1.2V | External regulator |
| VCC0P8 | 0.8V | Adjustable |
| VCC0P9 | 0.9V | External regulator |

---

## Crystal Requirements (KR)

| Parameter | Value |
|-----------|-------|
| Frequency | 25.000 MHz |
| Tolerance | ±30 ppm |
| Load Capacitance | 20 pF |
| ESR Max | 50Ω |

---

## Passive Components (From Datasheets)

### Pull-up/Pull-down Resistors
| Signal | Resistor | To |
|--------|----------|-----|
| I2C (LC GPIO) | 1kΩ | 1.8V_Sx |
| SMBUS | 330Ω | 1.8V_Sx |
| RESET_N | 10kΩ | GND |
| VBUS_EN | 100kΩ | GND |
| HPD | 100kΩ | GND |
| LSRX | 1MΩ | GND |
| LSTX | 20kΩ | 1.8V_Sx |

### SVR Inductors
| SVR | Inductance | Tolerance | DCR Max |
|-----|------------|-----------|---------|
| 0.75V | 0.4µH | ±20% | 8.3mΩ |
| 1.2V | 0.6µH | ±20% | 43mΩ |

### Ferrite Beads
| Application | Zin @ 1MHz | DCR Max |
|-------------|------------|---------|
| SVR Input | >5Ω | 20mΩ |

---

## Interfaces (From Datasheets)

### SPI Flash Requirements
| Parameter | Value |
|-----------|-------|
| Clock | 50 MHz minimum |
| Voltage | 1.8V |
| Sector Size | 4KB |
| Required Commands | WREN (0x06), WRDI (0x04), RDSR (0x05), Fast Read (0x0B), PP (0x02), SE (0x20), Dual Output (0x3B) |

---

## Still TODO

- [ ] FX20 part number and specs
- [ ] PMG1-S3 specific part number
- [ ] Connector part numbers (Type-C, M.2)
- [ ] PCB vendor selection
- [ ] Lead time confirmation
