# ThunderCat6 Schematic Blocks

## Document Control
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.2 | 2026-06-01 | - | Updated with KR/BR datasheet specs |

---

## Datasheet Sources
- ✅ Kite Ridge 0.76 (March 2026)
- ✅ Barlow Ridge Accessory Training v1.2
- ✅ Tornado Ridge 0.5 Draft
- [ ] FX20 - Still needed
- [ ] PMG1-S3 - Available from Infineon

---

## Block Diagram

```
UFP (Type-C) ──► [Signal Routing] ──► BR (TBT4 4-Port Hub)
                      │                   │
                      │                   ├──► M.2 SSD (PCIe Gen5)
                      │                   ├──► MST Hub (DP)
                      │                   └──► USB3
                      │
                      ├──► KR (USB4 Hub Controller)
                      │         │
                      │         └──► USB4 Ver2 (40Gbps Gen4)
                      │
                      └──► FX20 (USB Traffic Gen)
                                │
                                └──► DFP Ports
```

---

## BR (Barlow Ridge) GPIO Configuration

### LC GPIOs (1.8V_Sx Domain)
| GPIO# | Ball | Signal Name | Type | Board Config |
|-------|------|-------------|------|--------------|
| GPIO_0 | AC17 | PM_PCIE_S0_EN | OUT | 100kΩ PD to GND |
| GPIO_1 | AC18 | PM_MST_RST_N | OUT | 10kΩ PU to 1.8V_Sx |
| GPIO_3 | AC16 | I2C_SCL | OD | 1kΩ PU to 1.8V_Sx |
| GPIO_4 | AC8 | I2C_SDA | OD | 1kΩ PU to 1.8V_Sx |
| GPIO_7 | AC10 | TMU_CLKIN | IN | - |
| GPIO_8 | AC23 | TMU_CLKOUT | OUT | - |

### POC GPIOs (Power-On Control)
| GPIO# | Ball | Signal Name | Type | Board Config |
|-------|------|-------------|------|--------------|
| POC_GPIO_0 | L21 | PA_BIDIR_IN_EN | OUT | 100kΩ PD |
| POC_GPIO_1 | V21 | PB_BIDIR_IN_EN | OUT | 100kΩ PD |
| POC_GPIO_2 | AC22 | PAB_I2CINT_N | IN | 10kΩ PU to 1.8V_Sx |
| POC_GPIO_4 | K21 | PCIE_WAKE_N | IN | 10kΩ PU to 1.8V_Sx |
| POC_GPIO_5 | F13 | PM_PCIE_EN | OUT | 100kΩ PD |
| POC_GPIO_6 | M23 | FORCE_WAKE | IN | 10kΩ PD (offline FW update) |
| POC_GPIO_7 | N21 | PCIE_RESET_N | OUT | 10kΩ PD |
| POC_GPIO_8 | F11 | SMBUS_SCL | OD | 330Ω PU to 1.8V_Sx |
| POC_GPIO_9 | F12 | SMBUS_SDA | OD | 330Ω PU to 1.8V_Sx |

### BR Port Functions (Ports A-D)
| Signal | Port A | Port B | Port C | Port D |
|--------|--------|--------|--------|--------|
| I2C Interrupt | PAB_I2CINT_N | PAB_I2CINT_N | PCD_I2CINT_N | PCD_I2CINT_N |
| BIDIR_IN_EN | POC_GPIO_0 | POC_GPIO_1 | POC_GPIO_13 | POC_GPIO_11 |
| LSRX | POC_GPIO_16 | POC_GPIO_18 | POC_GPIO_20 | POC_GPIO_22 |
| LSTX | POC_GPIO_17 | POC_GPIO_19 | POC_GPIO_21 | POC_GPIO_23 |
| VBUS_EN | - | POC_GPIO_18 | POC_GPIO_20 | POC_GPIO_22 |

---

## KR (Kite Ridge) Interface Details

### I2C Interface
| Signal | Description |
|--------|-------------|
| I2C_SCL | Clock (Master/Slave configurable) |
| I2C_SDA | Data (Master/Slave configurable) |
| I2C_INT | Interrupt output |

**Transaction Format:** Start → Slave addr (7b + R/W) → Reg offset [7:0] → Size [7:0] → Data

### SPI Interface (For Flash)
| Parameter | Specification |
|-----------|---------------|
| Clock | 50 MHz minimum |
| Voltage | 1.8V |
| Sector Size | 4KB |

### Digital I/O Levels (1.8V)
| Parameter | Min | Max |
|-----------|-----|-----|
| VOH | 1.4V | - |
| VOL | - | 0.4V |
| VIH | 0.7×VCC | VCC+0.3V |
| VIL | -0.3V | 0.3×VCC |
| Internal PU | 31kΩ | 79kΩ |
| Internal PD | 31kΩ | 68kΩ |

### KR Reset Timing
```
VCC1P8_SX ─────┐
               │ 90% reached
               └─────────────────────
                     │ 100µs min
RESET_N  ────────────┘
              Rise time: 0.1-500ns
```

### KR SBU MUX Timing
- Minimum 20ms delay after mode entry acknowledgment before SBU MUX activation
- Isolation required in disconnect state

---

## TR (Tornado Ridge) - PCIe Mini Dock

### Operational Modes
| Mode | Description | PCIe Config |
|------|-------------|-------------|
| PCIe Mini Dock | TBT3/USB4 + PCIe tunneling | 4 lanes @ 32Gbps/lane |
| Storage | NVMe endpoint | Single NVMe |

### Bifurcation Options
- 1x4 (single x4 device)
- 4x1 (four x1 devices)
- 2x2 (two x2 devices)
- 1x2+2x1 (mixed)

### Protocol Support
- PCIe Gen5
- USB4 v2.0 (symmetric only)
- TBT Gen3
- USB3.2 Gen2x2 / Gen2x1

---

## Power Distribution

### SVR Configuration (BR)
```
              ┌─────────────┐
 VIN ───FB───►│  0.75V SVR  │───► VCC0P8 (3A max)
              │  L=0.4µH    │
              └─────────────┘
                    │
              6×22µF Cout

              ┌─────────────┐
 VIN ───FB───►│  1.2V ASVR  │───► VCC1P2 (1A max)
              │  L=0.6µH    │
              └─────────────┘
                    │
              4×22µF Cout
```

### Power Rails Required
| Rail | Voltage | Max Current | Source |
|------|---------|-------------|--------|
| VCC1P8_SX | 1.8V | 200mA (KR) | External LDO |
| VCC1P8_SX_IO | 1.8V | 100mA (KR) | External LDO |
| VCC1P2 | 1.2V | 1250mA (KR) | BR ASVR or External |
| VCC0P8 | 0.8V | 4A (KR) | BR SVR |
| VCC0P9 | 0.9V | TBD (TR) | External |

---

## Test Points Required

| TP# | Signal | Purpose |
|-----|--------|---------|
| TP1 | GND | Ground reference |
| TP2 | VCC1P8_SX | 1.8V power rail |
| TP3 | VCC1P2 | 1.2V power rail |
| TP4 | VCC0P8 | 0.8V power rail |
| TP5 | I2C_SCL | I2C clock |
| TP6 | I2C_SDA | I2C data |
| TP7 | SMBUS_SCL | SMBUS clock |
| TP8 | SMBUS_SDA | SMBUS data |
| TP9 | RESET_N | Reset signal |
| TP10 | FORCE_WAKE | FW update trigger |
| TP11 | THERMDA | Thermal diode |

---

## Thermal Monitoring

### KR Thermal Diode
**Equation:** Tj [°C] = 600.52 – 712.02 × V[V] (at 1mA)

| Junction Temp | Diode Voltage |
|---------------|---------------|
| 25°C | 0.808V |
| 55°C | 0.766V |
| 110°C | 0.689V |

---

## Still TODO

- [ ] FX20 pin configuration
- [ ] PMG1-S3 pin configuration
- [ ] MST Hub (RTD2198) configuration
- [ ] Type-C connector pinout
- [ ] M.2 socket pinout
- [ ] External SBU MUX selection (KR doesn't have internal SBU switching)
