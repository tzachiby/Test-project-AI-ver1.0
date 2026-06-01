# ThunderCat6 Firmware Architecture

## Document Control
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.2 | 2026-06-01 | - | Updated with KR/BR/TR datasheet specs |

---

## Datasheet Sources
- ✅ Kite Ridge 0.76 (March 2026)
- ✅ Barlow Ridge Accessory Training v1.2
- ✅ Tornado Ridge 0.5 Draft
- [ ] FX20 - Still needed from Infineon

---

## KR (Kite Ridge) Firmware

### Communication Interfaces

#### I2C Interface
| Parameter | Specification |
|-----------|---------------|
| Signals | I2C_SCL, I2C_SDA, I2C_INT |
| Mode | Master or Slave (configurable) |
| Transaction | Start → Slave addr (7b + R/W) → Reg offset [7:0] → Size [7:0] → Data |

#### SPI Flash Interface
| Parameter | Specification |
|-----------|---------------|
| Clock | 50 MHz minimum |
| Voltage | 1.8V |
| Sector Size | 4KB |

**Required SPI Commands:**
| Command | Opcode |
|---------|--------|
| WREN (Write Enable) | 0x06 |
| WRDI (Write Disable) | 0x04 |
| RDSR (Read Status) | 0x05 |
| Fast Read | 0x0B |
| PP (Page Program) | 0x02 |
| SE (Sector Erase) | 0x20 |
| Dual Output | 0x3B / 0xBB |

### Supported Protocols
| Protocol | Speed |
|----------|-------|
| USB4 Ver2 Gen4 | 40Gbps (PAM3) |
| USB4 Ver2 Gen3 | 20.625/20.0Gbps |
| USB4 Ver2 Gen2 | 10.3125/10.0Gbps |
| USB3.2 Gen2x2 | 20Gbps |
| USB3.2 Gen2x1 | 10Gbps |
| DisplayPort UHBR20G | 20Gbps |
| DisplayPort UHBR10G | 10Gbps |
| DisplayPort HBR3 | 8.1Gbps |
| PCIe Gen5 | Tunneling support |
| TBT Gen3 | Compatible |

---

## BR (Barlow Ridge) Firmware

### SMBUS Interface (For FW Update)
| Parameter | Specification |
|-----------|---------------|
| Signals | SMBUS_SCL (POC_GPIO_8), SMBUS_SDA (POC_GPIO_9) |
| Pull-ups | 330Ω to 1.8V_Sx |
| FW Update Trigger | FORCE_WAKE (POC_GPIO_6) with 10kΩ PD |

### GPIO Control Signals
| Function | GPIO | Type | Purpose |
|----------|------|------|---------|
| PCIe S0 Enable | GPIO_0 (AC17) | OUT | PCIe power control |
| MST Reset | GPIO_1 (AC18) | OUT | Reset MST hub |
| PCIe Enable | POC_GPIO_5 (F13) | OUT | PCIe power enable |
| PCIe Reset | POC_GPIO_7 (N21) | OUT | PCIe reset control |
| PCIe Wake | POC_GPIO_4 (K21) | IN | Wake from PCIe |

### SVR Control
| SVR | Output Range | Step | Control Method |
|-----|--------------|------|----------------|
| 0.75V SVR | 0.67-0.924V | 1.0mV (256 steps) | SVR_CNTL register |
| 1.2V ASVR | 1.07-1.47V | 1.6mV (256 steps) | ASVR_CNTL register |

---

## TR (Tornado Ridge) Firmware

### SMBUS FW Update
| Parameter | Specification |
|-----------|---------------|
| Max Transaction | 128 bytes |
| NAK Retry Delay | 10ms minimum |
| Trigger | FORCE_WAKE signal |

### Operational Modes
| Mode | Configuration |
|------|---------------|
| PCIe Mini Dock | TBT3/USB4 + PCIe tunneling, 4 lanes @ 32Gbps/lane |
| Storage | Single NVMe endpoint via USB4/TBT3/USB3/MFDP |

### PCIe Bifurcation
| Config | Lanes |
|--------|-------|
| 1x4 | Single x4 device |
| 4x1 | Four x1 devices |
| 2x2 | Two x2 devices |
| 1x2+2x1 | Mixed configuration |

---

## Power Sequencing

### KR Reset Sequence
```
1. Apply VCC1P8_SX
2. Wait for VCC1P8_SX to reach 90%
3. Wait minimum 100µs
4. Deassert RESET_N (rise time 0.1-500ns)
```

### SBU MUX Timing
- Wait minimum 20ms after mode entry acknowledgment
- Isolate SBU in disconnect state

---

## Thermal Monitoring

### KR Thermal Diode
**Equation:** Tj [°C] = 600.52 – 712.02 × V[V] (at 1mA)

**Implementation:**
```python
def read_junction_temp(voltage_v: float) -> float:
    """
    Calculate junction temperature from thermal diode voltage.
    Args:
        voltage_v: Diode voltage at 1mA bias
    Returns:
        Junction temperature in °C
    """
    return 600.52 - 712.02 * voltage_v
```

---

## Crystal Requirements

| Parameter | Value |
|-----------|-------|
| Frequency | 25.000 MHz |
| Tolerance | ±30 ppm @ 25°C |
| Load Capacitance | 20 pF |
| ESR Max | 50Ω |

---

## Still TODO

- [ ] FX20 firmware/SDK documentation
- [ ] PMG1-S3 EZ-PD Configurator settings
- [ ] Complete register map from full datasheets
- [ ] Firmware update procedures validation
