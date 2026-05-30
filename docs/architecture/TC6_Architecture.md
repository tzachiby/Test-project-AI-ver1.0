# ThunderCat6 Architecture Document

## Document Control
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-05-25 | AI Assistant | Initial draft |

---

## 1. System Overview

ThunderCat6 (TC6) is a test card designed to validate Thunderbolt 4, USB4, and USB3.2 functionality on Intel platforms. The architecture addresses TC5 limitations while adding new capabilities for next-generation platform validation.

---

## 2. High-Level Block Diagram

```
                                    ┌─────────────────────────────────────────────────────────────┐
                                    │                    ThunderCat6 Test Card                     │
                                    │                                                              │
    ┌────────┐                      │  ┌─────────────┐       ┌─────────────┐                      │
    │  DUT   │◄─────────────────────┼──┤     UFP     │       │   Backdoor  │                      │
    │(Target)│     Type-C Cable     │  │  (Type-C)   │       │   Mini-USB  │──────┐               │
    └────────┘                      │  └──────┬──────┘       └──────┬──────┘      │               │
                                    │         │                      │            │               │
                                    │         ▼                      ▼            │               │
                                    │  ┌──────────────┐       ┌─────────────┐     │               │
                                    │  │  High-Speed  │       │    FTDI     │◄────┤               │
                                    │  │     Mux      │       │  FT4232H    │     │               │
                                    │  └──────┬───────┘       └──────┬──────┘     │               │
                                    │         │                      │            │               │
                                    │    ┌────┴────┬────────┬───────┴───────┐    │               │
                                    │    ▼         ▼        ▼               ▼    │               │
                                    │ ┌─────┐  ┌─────┐  ┌─────────┐    ┌──────┐  │   ┌─────────┐ │
                                    │ │ BR  │  │ KR  │  │  FX20   │    │ USB2 │  │   │  Host   │ │
                                    │ │(TBT)│  │(USB4│  │(Traffic │    │ Hub  │  └───┤   PC    │ │
                                    │ └──┬──┘  └──┬──┘  │  Gen)   │    └──┬───┘      └─────────┘ │
                                    │    │        │     └────┬────┘       │                      │
                                    │    │        │          │            │                      │
                                    │    └────┬───┴──────────┴────────────┘                      │
                                    │         │                                                   │
                                    │         ▼                                                   │
                                    │  ┌──────────────────────────────────────────────────┐      │
                                    │  │                  Internal Bus                     │      │
                                    │  └──────┬────────────┬────────────┬─────────────────┘      │
                                    │         │            │            │                         │
                                    │         ▼            ▼            ▼                         │
                                    │  ┌───────────┐ ┌───────────┐ ┌───────────┐                 │
                                    │  │   M.2     │ │   MST     │ │    PD     │                 │
                                    │  │   SSD     │ │  Realtek  │ │ PMG1-S3   │                 │
                                    │  │  (PCIe)   │ │(DP Sink)  │ │ x2        │                 │
                                    │  └───────────┘ └─────┬─────┘ └───────────┘                 │
                                    │                      │                                      │
                                    │                      ▼                                      │
                                    │               ┌──────────────┐                             │
                                    │               │   DFP x2     │                             │
                                    │               │  (Type-C)    │                             │
                                    │               └──────────────┘                             │
                                    │                      │                                      │
                                    └──────────────────────┼──────────────────────────────────────┘
                                                           │
                                                           ▼
                                                    ┌──────────────┐
                                                    │   External   │
                                                    │   Devices    │
                                                    └──────────────┘
```

---

## 3. Component Architecture

### 3.1 Main Controllers

#### 3.1.1 Barlow Ridge (BR) - Thunderbolt 4 Controller
- **Function**: TBT3/TBT4 tunneling, PCIe, DP, USB
- **Interface**: PCIe Gen4 x4 to SSD, DP2.0 to MST
- **Control**: SPI/I2C from FTDI

#### 3.1.2 Kite Ridge (KR) - USB4 Controller (NEW)
- **Function**: USB4 v1/v2 support, rate control
- **Interface**: USB4 to UFP
- **Control**: I2C from FTDI
- **Note**: Enables USB4 Gen2/Gen3 downgrade testing

#### 3.1.3 FX20 - USB Traffic Generator (Replaces FX3)
- **Function**: USB synthetic traffic generation
- **Capabilities**:
  - USB 3.2 Gen1/Gen2/Gen2x2 (5/10/20 Gbps)
  - USB 2.0 High-Speed
  - LPM support (U1, U2, U3, Deep Sleep)
  - Bulk, Interrupt, Isoc protocols
- **Control**: I2C/SPI from FTDI

### 3.2 Connectivity Components

#### 3.2.1 High-Speed Mux (NEW)
- **Function**: Route UFP signals to different paths
- **Paths**:
  1. UFP → BR (TBT/USB4 tunnel)
  2. UFP → KR (USB4 native)
  3. UFP → FX20 (USB native, bypassing BR)
  4. UFP → DFP (Direct pass-through)
- **Control**: I2C/GPIO from FTDI

#### 3.2.2 USB2 Hub
- **Function**: USB2.0 routing and hub functionality
- **Ports**: Internal distribution
- **Control**: I2C from FTDI

#### 3.2.3 Low-Speed Mux (NEW)
- **Function**: Control signal routing
- **Control**: GPIO from FTDI

### 3.3 Display Components

#### 3.3.1 MST Realtek Hub (RTD2198)
- **Function**: Multi-Stream Transport hub for DP
- **Capabilities**:
  - DP 2.0/2.1 support
  - Up to 4 displays (2 for PPV, 4 for FV)
  - SST mode support (NEW - requires FW)
  - CRC calculation for glitch detection
- **Interface**: DP from BR, Type-C DFP outputs

### 3.4 Storage

#### 3.4.1 M.2 SSD Socket
- **Function**: PCIe Gen4 x4 NVMe storage
- **Form Factor**: M.2 2280 (2230 alternative for size constraints)
- **Interface**: PCIe x4 tunneled through BR

### 3.5 Power Delivery

#### 3.5.1 PD Controller (PMG1-S3 x2)
- **Function**: USB-PD negotiation and control
- **Capabilities**:
  - Rate control for USB/DP downgrade
  - Dual PD for enhanced control
  - Replaces separate PD + DMC
- **Control**: I2C from FTDI

### 3.6 Control & Debug

#### 3.6.1 FTDI FT4232H
- **Function**: Backdoor host interface
- **Capabilities**:
  - 4-channel USB-UART/FIFO
  - I2C/SPI/GPIO master
  - DIP switch reading
  - FW programming interface
- **Interface**: Mini-USB to Host PC

#### 3.6.2 DIP Switches
- **Bits**: 4 (16 values)
- **Function**: Card identification and default mode

#### 3.6.3 Status LEDs
- **Green**: Power status
- **Blue**: USB/PCIe activity
- **Red**: Errors
- **Yellow**: Reset indicators

---

## 4. Signal Flow Diagrams

### 4.1 USB4 Tunneled Mode
```
DUT → UFP → HS Mux → BR → Internal Bus → SSD/FX20/MST
```

### 4.2 USB Native Mode (NEW)
```
DUT → UFP → HS Mux → FX20 (Direct, bypassing BR)
```

### 4.3 DP Alt Mode
```
DUT → UFP → HS Mux → BR → MST → DFP → External Display
```

### 4.4 External Device Pass-through (NEW)
```
DUT → UFP → HS Mux → DFP → Commercial Device
```

---

## 5. Control Architecture

### 5.1 Command Flow
```
Host PC → Mini-USB → FTDI → I2C/SPI/GPIO → Components
```

### 5.2 Control Interfaces

| Component | Interface | Address/Channel |
|-----------|-----------|-----------------|
| BR | SPI/I2C | TBD |
| KR | I2C | TBD |
| FX20 | I2C | TBD |
| PD (x2) | I2C | TBD |
| MST | I2C | TBD |
| HS Mux | I2C/GPIO | TBD |
| USB2 Hub | I2C | TBD |

---

## 6. Power Architecture

### 6.1 Power Input
- **External**: 12V DC (primary)
- **On-board regulators**: 5V, 3.3V, 1.8V as needed

### 6.2 Power Distribution
```
12V Input → Power Switch → Regulators → Components
                ↓
           Power LEDs
```

### 6.3 Back-Drive Prevention
- No residual voltage on Type-C when DUT is OFF
- Same implementation as TC4

---

## 7. Mechanical Specifications

| Parameter | Specification |
|-----------|---------------|
| Form Factor | ThunderCat3.0 compatible |
| Max Component Height | Same as TC3.0 primary side |
| Secondary Side | No components |
| Mounting Holes | TC3.0 compatible positions |
| Backdoor Connector | Mini-USB (same location as previous) |
| M.2 Socket | 2280 (2230 alternative) |

---

## 8. Programming Interfaces

| Component | Programming Method |
|-----------|-------------------|
| BR | TenLira via UFP/Backdoor |
| KR | TBD |
| DMC/PD | Cypress Ezprog (50mil header) |
| FX20 | I2C/SPI via Backdoor |
| SSD | Via Backdoor USB (NEW) |
| BLT EEPROM | Via Backdoor USB |

---

## 9. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-05-25 | Initial architecture based on TC6 requirements |
