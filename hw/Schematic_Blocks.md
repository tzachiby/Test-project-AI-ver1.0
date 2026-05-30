# ThunderCat6 Schematic Design Blocks

## 1. Power Distribution

```
                    12V Input (J6)
                         │
                         ▼
                    ┌─────────┐
                    │  Fuse   │
                    │  5A     │
                    └────┬────┘
                         │
              ┌──────────┼──────────┐
              │          │          │
              ▼          ▼          ▼
         ┌────────┐ ┌────────┐ ┌────────┐
         │  VR1   │ │Direct  │ │Direct  │
         │12V→5V  │ │  12V   │ │  12V   │
         │ 3A    │ │ to SSD │ │ to BR  │
         └───┬────┘ └────────┘ └────────┘
             │
    ┌────────┼────────┐
    │        │        │
    ▼        ▼        ▼
┌──────┐ ┌──────┐ ┌──────┐
│ VR2  │ │ VR3  │ │ VR4  │
│5V→3.3│ │3.3→1.8│ │3.3→1.1│
│ 2A   │ │ 1A   │ │ 1A   │
└──────┘ └──────┘ └──────┘
    │        │        │
    ▼        ▼        ▼
  3.3V     1.8V     1.1V
```

## 2. UFP (Type-C) Interface

```
         Type-C Connector (J1)
    ┌──────────────────────────────┐
    │  CC1  CC2  SBU1  SBU2       │
    │  TX1± TX2± RX1± RX2±        │
    │  D+   D-   VBUS  GND        │
    └──────┬───────────────────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌───────┐    ┌────────────┐
│ PMG1  │    │ High-Speed │
│ (PD)  │    │    Mux     │
│ U5A   │    │    U8      │
└───┬───┘    └──────┬─────┘
    │               │
    │    ┌──────────┼──────────┬──────────┐
    │    │          │          │          │
    │    ▼          ▼          ▼          ▼
    │  ┌───┐     ┌───┐     ┌─────┐    ┌─────┐
    │  │BR │     │KR │     │FX20 │    │ DFP │
    │  │U1 │     │U2 │     │ U3  │    │Pass │
    │  └───┘     └───┘     └─────┘    └─────┘
    │
    └──► FTDI (Control)
```

## 3. High-Speed Mux Routing

```
                 UFP SS Lines (TX/RX)
                         │
                         ▼
              ┌─────────────────────┐
              │   High-Speed Mux    │
              │      PI3USB30532    │
              │                     │
              │  SEL[2:0] ◄─── FTDI │
              └──┬────┬────┬────┬───┘
                 │    │    │    │
    Path 0 ──────┘    │    │    └────── Path 3
    (BR)              │    │            (DFP1)
                      │    │
         Path 1 ──────┘    └────── Path 2
         (KR)                      (FX20)
```

## 4. Barlow Ridge (BR) Block

```
                    From HS Mux
                         │
                         ▼
    ┌─────────────────────────────────────┐
    │         Barlow Ridge (U1)           │
    │                                     │
    │  USB4/TBT ◄──── UFP                │
    │                                     │
    │  PCIe x4  ────► M.2 SSD            │
    │                                     │
    │  DP OUT   ────► MST Hub            │
    │                                     │
    │  USB3     ────► ASMedia/FX20       │
    │                                     │
    │  I2C/SPI  ◄──── FTDI Control       │
    │                                     │
    │  SPI Flash ◄──► External EEPROM    │
    └─────────────────────────────────────┘
```

## 5. FX20 USB Traffic Generator

```
                    From HS Mux (Direct Path)
                              │
                              ▼
    ┌───────────────────────────────────────┐
    │            FX20 (U3)                  │
    │                                       │
    │  USB3.2 ◄──── Super Speed Lines      │
    │  USB2.0 ◄──── High Speed Lines       │
    │                                       │
    │  ┌─────────────────────────────────┐ │
    │  │      Internal Features          │ │
    │  │  • Gen1/Gen2/Gen2x2 Support    │ │
    │  │  • LPM (U1/U2/U3/Deep Sleep)   │ │
    │  │  • Bulk/Interrupt/Isoc         │ │
    │  │  • Loopback Mode               │ │
    │  └─────────────────────────────────┘ │
    │                                       │
    │  I2C      ◄──── FTDI Control         │
    │  RESET_N  ◄──── FTDI GPIO            │
    │  INT      ────► FTDI GPIO            │
    └───────────────────────────────────────┘
```

## 6. MST Hub (Display)

```
                    DP from BR
                         │
                         ▼
    ┌─────────────────────────────────────┐
    │         RTD2198 MST Hub (U4)        │
    │                                     │
    │  DP IN   ◄──── From BR/Alt Mode    │
    │                                     │
    │  DP OUT1 ────► DFP1 (Type-C)       │
    │  DP OUT2 ────► DFP2 (Type-C)       │
    │  DP OUT3 ────► Internal Sink       │
    │  DP OUT4 ────► Internal Sink       │
    │                                     │
    │  I2C     ◄──── FTDI Control        │
    │  HPD     ◄──► GPIO Control         │
    │  AUX     ◄──► DPCD Interface       │
    │                                     │
    │  Mode: MST / SST (FW Selectable)   │
    └─────────────────────────────────────┘
```

## 7. FTDI Backdoor Controller

```
    Mini-USB (J4) ◄──── Host PC
           │
           ▼
    ┌─────────────────────────────────────┐
    │         FT4232H (U7)                │
    │                                     │
    │  Channel A: UART (Debug Console)   │
    │  Channel B: I2C Master             │
    │  Channel C: SPI Master             │
    │  Channel D: GPIO                   │
    │                                     │
    │  GPIO Allocation:                   │
    │  ├─ GPIO[2:0] → HS Mux Select      │
    │  ├─ GPIO[3]   → BR Reset           │
    │  ├─ GPIO[4]   → KR Reset           │
    │  ├─ GPIO[5]   → FX20 Reset         │
    │  ├─ GPIO[6]   → MST Reset          │
    │  ├─ GPIO[7]   → LED Control        │
    │  └─ GPIO[11:8]← DIP Switch Read    │
    │                                     │
    │  EEPROM ◄──► 93C46 (Config)        │
    └─────────────────────────────────────┘
```

## 8. DIP Switch & ID

```
    ┌───────────────────┐
    │  4-bit DIP Switch │
    │   SW1 (CTS 219)   │
    │                   │
    │  [1][2][3][4]     │
    │   │  │  │  │      │
    └───┼──┼──┼──┼──────┘
        │  │  │  │
        ▼  ▼  ▼  ▼
    ┌───────────────────┐
    │  Pull-up 10K      │
    │  to 3.3V          │
    └─────────┬─────────┘
              │
              ▼
         FTDI GPIO[11:8]

    DIP Values:
    0x0 = TBT3 Tunnel
    0x1 = TBT4 Tunnel
    0x2 = USB4 Tunnel
    0x3 = USB3 Gen2x2
    0x4 = USB3 Gen1x1
    0x5 = DP Alt Mode
    0x6 = MFD Mode
    0x7 = Passthrough
    0x8 = Gen T PCIe x4
    0x9 = Gen T PCIe x2
    0xA = Gen T PCIe x1
    0xB = Gen T Mixed (PCIe+DP)
    0xC = Gen T Bandwidth Test
    0xD-0xF = Reserved
```

## 9. Status LEDs

```
    ┌─────────────────────────────────────┐
    │           LED Array                 │
    │                                     │
    │  LED1 (Green)  ── 3.3V Power Good  │
    │  LED2 (Blue)   ── TBT/USB4 Link    │
    │  LED3 (Blue)   ── USB3 Activity    │
    │  LED4 (Blue)   ── DP Link          │
    │  LED5 (Blue)   ── PCIe Activity    │
    │  LED6 (Red)    ── Error            │
    │  LED7 (Yellow) ── Reset Active     │
    │                                     │
    │  All driven via FTDI GPIO or       │
    │  direct signal monitoring          │
    └─────────────────────────────────────┘
```

## 10. M.2 SSD Socket

```
    ┌─────────────────────────────────────┐
    │        M.2 Socket (J5)              │
    │        Key-M, 2280                  │
    │                                     │
    │  PCIe x4  ◄──── BR PCIe Port       │
    │  SATA     ──── Not Connected       │
    │  USB      ──── Optional USB Path   │
    │                                     │
    │  3.3V     ◄──── Power Rail         │
    │  PERST#   ◄──── BR Control         │
    │  CLKREQ#  ────► BR                 │
    │  PEWAKE#  ────► BR                 │
    └─────────────────────────────────────┘
```

---

## Pin Assignments Summary

### Type-C UFP (J1)
| Pin | Signal | Description |
|-----|--------|-------------|
| A1/B12 | GND | Ground |
| A2/B11 | TX1+/- | SuperSpeed TX |
| A3/B10 | TX2+/- | SuperSpeed TX |
| A4/B9 | VBUS | Power (5V/12V) |
| A5/B8 | CC1/CC2 | Configuration Channel |
| A6/B7 | D+/D- | USB 2.0 |
| A7/B6 | SBU1/SBU2 | Sideband Use |
| A8/B5 | RX2+/- | SuperSpeed RX |
| A9/B4 | RX1+/- | SuperSpeed RX |

### FTDI I2C Bus Addresses
| Device | Address | Description |
|--------|---------|-------------|
| FX20 | 0x68 | USB Traffic Generator |
| MST Hub | 0x50 | Realtek RTD2198 |
| PD Controller | 0x40 | PMG1-S3 |
| EEPROM | 0x54 | BLT Config Storage |
| Retimer | 0x60 | DS100BR410 |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| 0.1 | 2026-05-30 | AI | Initial schematic blocks |
