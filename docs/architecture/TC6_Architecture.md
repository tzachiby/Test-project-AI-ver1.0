# ThunderCat6 System Architecture

## Document Control
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.2 | 2026-06-01 | - | Updated with KR/BR/TR datasheet specs |

---

## Datasheet Sources
- ✅ Kite Ridge 0.76 (March 2026)
- ✅ Barlow Ridge Accessory Training v1.2
- ✅ Tornado Ridge 0.5 Draft (July 2025)
- [ ] FX20 - Still needed from Infineon
- [ ] PMG1-S3 - Available from Infineon

---

## High-Level Block Diagram

```
┌───────────────────────────────────────────────────────────────────────────┐
│                           ThunderCat6 Test Card                           │
│                                                                           │
│  UFP (Type-C) ──┬──► BR (TBT4 4-Port Hub) ──┬──► M.2 SSD (PCIe Gen5)     │
│                 │                            ├──► MST RTD2198 (DP)        │
│                 │                            └──► USB3 Ports              │
│                 │                                                         │
│                 ├──► KR (USB4 Hub) ──► USB4 Ver2 40Gbps (DFP)            │
│                 │                                                         │
│                 ├──► TR (PCIe Mini Dock) ──► NVMe (Optional)             │
│                 │                                                         │
│                 └──► FX20 (USB Traffic) ──► DFP Loopback/Sink            │
│                                                                           │
│  PMG1-S3 x2 ◄──► CC Control (UFP/DFP PD)                                 │
│                                                                           │
│  Backdoor (FTDI) ◄──► I2C Bus ◄──► All Controllers                       │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## Main Components

| Component | Version | Function | Datasheet Status |
|-----------|---------|----------|------------------|
| BR (Barlow Ridge) | v1.2 | TBT4 4-Port Hub Controller | ✅ Available |
| KR (Kite Ridge) | 0.76 | USB4 Hub Controller | ✅ Available |
| TR (Tornado Ridge) | 0.5 | PCIe Mini Dock (KR-based) | ✅ Draft Available |
| FX20 | - | USB Traffic Generator | ❌ Needed |
| PMG1-S3 | - | USB-PD Controller x2 | ⚠️ Available (need to download) |
| MST RTD2198 | - | DP Sink Hub x4 | ❌ Needed |

---

## Protocol Support Matrix

### KR (Kite Ridge) - USB4 Hub
| Protocol | Speed | Notes |
|----------|-------|-------|
| USB4 Ver2 Gen4 | 40Gbps | PAM3 signaling |
| USB4 Ver2 Gen3 | 20.625/20.0Gbps | |
| USB4 Ver2 Gen2 | 10.3125/10.0Gbps | |
| USB3.2 Gen2x2 | 20Gbps | |
| USB3.2 Gen2x1 | 10Gbps | |
| DisplayPort UHBR20G | 20Gbps | |
| DisplayPort UHBR10G | 10Gbps | |
| PCIe Gen5 | Tunneling | Via USB4 |
| TBT Gen3 | Compatible | |

### BR (Barlow Ridge) - TBT4 Hub
| Feature | Details |
|---------|---------|
| Ports | 4 Type-C DFP + 1 UFP |
| PCIe | Gen5 tunneling |
| DP | Alt Mode support |
| USB3 | Gen2 |

### TR (Tornado Ridge) - Mini Dock
| Mode | Description |
|------|-------------|
| PCIe Mini Dock | 4 lanes @ 32Gbps/lane, TBT3/USB4 + PCIe tunneling |
| Storage | Single NVMe endpoint |
| Protocols | USB4 v2.0 (symmetric), TBT Gen3, USB3.2 Gen2x2, PCIe Gen5 |

---

## I2C Bus Architecture

```
                     ┌────────────┐
                     │ Backdoor   │
                     │  (FTDI)    │
                     └─────┬──────┘
                           │ I2C Master
         ┌─────────────────┼─────────────────┐
         │                 │                 │
   ┌─────┴─────┐    ┌──────┴─────┐    ┌──────┴─────┐
   │    BR     │    │     KR     │    │   FX20    │
   │ LC GPIO   │    │  I2C I/F   │    │  I2C I/F  │
   │ 3/4       │    └────────────┘    └───────────┘
   └───────────┘
         │
   ┌─────┴─────┐
   │  SMBUS    │ (POC GPIO 8/9 - 330Ω PU)
   └───────────┘
```

### I2C Configuration
| Interface | Signals | Pull-ups | Domain |
|-----------|---------|----------|--------|
| BR LC I2C | GPIO_3 (AC16), GPIO_4 (AC8) | 1kΩ to 1.8V_Sx | LC GPIO |
| BR SMBUS | POC_GPIO_8 (F11), POC_GPIO_9 (F12) | 330Ω to 1.8V_Sx | POC GPIO |
| KR I2C | I2C_SCL, I2C_SDA, I2C_INT | External | Configurable M/S |

### KR I2C Transaction Format
```
START → Slave Addr (7b + R/W) → Reg Offset [7:0] → Size [7:0] → Data → STOP
```

---

## Power Architecture

### Power Rails Summary
| Rail | Voltage | Tolerance | Max Current | Source |
|------|---------|-----------|-------------|--------|
| VCC1P8_SX | 1.8V | 1.71-1.89V | 300mA total | External LDO |
| VCC1P8_SX_IO | 1.8V | - | 100mA (KR) | External LDO |
| VCC1P2 | 1.2V | 1.14-1.26V | 1250mA (KR) + 1A (BR) | BR ASVR / External |
| VCC0P8 | 0.8V | 0.7-0.9V | 4A (KR) + 3A (BR) | BR SVR |
| VCC0P9 | 0.9V | - | TBD (TR) | External |

### BR Switching Voltage Regulators
| SVR | Output | Steps | Max Current | Inductor |
|-----|--------|-------|-------------|----------|
| 0.75V SVR | 0.67-0.924V | 256 (1mV) | 3A | 0.4µH ±20% |
| 1.2V ASVR | 1.07-1.47V | 256 (1.6mV) | 1A | 0.6µH ±20% |

---

## Reset and Power-On Sequence

### KR Reset Requirements
```
         ┌──────────────────────────────────────────
VCC1P8_SX│           90% threshold
         │
         └──────────────────┐
                            │ 100µs min
                            ▼
RESET_N  ───────────────────┘ (Rise: 0.1-500ns)
```

### SBU MUX Timing
- Minimum 20ms delay after mode entry acknowledgment
- Isolate SBU signals in disconnect state

### BR FORCE_WAKE (FW Update)
- POC_GPIO_6 (M23) with 10kΩ pull-down
- Assert to trigger offline firmware update mode

---

## Thermal Monitoring

### KR Internal Thermal Diode
| Parameter | Value |
|-----------|-------|
| Equation | Tj [°C] = 600.52 – 712.02 × V[V] |
| Bias Current | 1mA |
| Access | THERMDA pin |

| Temperature | Diode Voltage |
|-------------|---------------|
| 25°C | 0.808V |
| 55°C | 0.766V |
| 110°C | 0.689V |

---

## Signal Routing Summary

### UFP → BR (TBT4 Path)
| Signal | Description |
|--------|-------------|
| USB4/TBT | Main tunnel (40Gbps Gen4) |
| DP AUX | Display configuration |
| CC1/CC2 | PD communication (via PMG1-S3) |
| SBU1/SBU2 | Sideband (external MUX required for KR) |

### BR → Downstream
| Port | Connection |
|------|------------|
| PCIe | M.2 SSD (Gen5 x4) |
| DP OUT | MST Hub (RTD2198) |
| USB3 | USB Hub / Direct |

---

## Clock Requirements

### KR Crystal
| Parameter | Value |
|-----------|-------|
| Frequency | 25.000 MHz |
| Tolerance | ±30 ppm |
| Load Capacitance | 20 pF |
| ESR Max | 50Ω |

---

## Still TODO

- [ ] FX20 integration details
- [ ] PMG1-S3 PDO configuration
- [ ] MST Hub routing
- [ ] Complete GPIO allocation table
- [ ] Power sequencing state machine
