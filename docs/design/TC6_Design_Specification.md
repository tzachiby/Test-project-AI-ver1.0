# ThunderCat6 Design Specification

## Document Control
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-05-25 | AI Assistant | Initial design based on TC6 requirements and TC5 feedback |

---

## 1. Design Overview

### 1.1 Purpose
ThunderCat6 (TC6) is a next-generation test card designed to validate Thunderbolt 4, USB4, and USB3.2 functionality on Intel platforms. This design addresses all showstopper and high-priority issues identified from TC5 deployment.

### 1.2 Design Goals
1. **Full USB speed downgrade support** - Gen1x1, Gen1x2, Gen2x1, Gen2x2
2. **Direct UFP-DFP bypass** - Commercial device testing without BR
3. **Enhanced DP support** - SST mode, UHBR13.5, variable LTTPR
4. **Faster mode switching** - Target <0.5 seconds
5. **FX20 integration** - Full LPM support (U1/U2/U3/Deep Sleep)
6. **Cost optimization** - TC6 FV ~30% cheaper than TC5

---

## 2. Key Design Decisions

### 2.1 Showstopper #1: Native USB Speed Downgrade
**Problem**: TC5 cannot control BR USB Hub rate/width in Native USB mode.

**Solution**: 
```
┌─────┐    ┌──────────────┐    ┌──────┐
│ UFP │───►│ High-Speed   │───►│ FX20 │  (Direct path, bypassing BR)
│     │    │    Mux       │    │      │
└─────┘    └──────────────┘    └──────┘
```
- Add high-speed mux between UFP and internal components
- FX20 connects directly to UFP via mux (bypassing BR)
- Rate control via FX20 register settings
- Supports all Gen configs: Gen1x1, Gen1x2, Gen2x1, Gen2x2

### 2.2 Showstopper #2: MFD USB/DP Rate Downgrade
**Problem**: Cannot control USB/DP rates in Multi-Function Device mode via BR.

**Solution**:
- Implement PD-based rate control exploration (Oded.D/Shay action item)
- Use high-speed mux to route MFD signals
- PD controller (PMG1-S3) handles rate negotiation

### 2.3 Showstopper #3: Variable LTTPR Configuration
**Problem**: No support for variable number of LTTPRs in DP path.

**Solution**:
- Add external retimer(s) with bypass capability
- Retimer can be enabled/disabled via I2C control
- Maximum retimers TBD based on board space

### 2.4 Showstopper #4: DP SST Mode
**Problem**: Current "SST" is just limiting MST to 1 display.

**Solution**:
- Use Realtek RTD2198 with SST mode FW
- Supports true SST with independent HPD per display
- DP1.4 HBR3 in both MST and SST modes

### 2.5 Showstopper #5: USB4 Rate Downgrade
**Problem**: Cannot downgrade USB4v1 to Gen3/Gen2.

**Solution**:
- PD control for rate negotiation
- USB4 always 1+1 bonding, lanes via active cable
- KR (Kite Ridge) integration for native USB4 control

### 2.6 High Priority #6: BR Bypass for Commercial Devices
**Problem**: No bypass channel without going through BR.

**Solution**:
```
Option 1: UFP ───► HS Mux ───► FX20 (USB3 only)
Option 2: UFP ───► HS Mux ───► DFP (External device connector)
```

### 2.7 High Priority #8: LPM Support
**Problem**: TC5's FX3 lacks Low Power Mode support.

**Solution**: FX20 replaces FX3 with full LPM support:
- U0: Active mode (5/10/20 Gbps)
- U1/U2: USB3 low-power modes
- U3: Suspend mode
- Deep Sleep: Minimal power

### 2.8 High Priority #9: Native HDMI/DP Module
**Problem**: Cannot switch between native HDMI and DP without external cables.

**Solution**: Explore on-board HDMI/DP connectivity options (TBD)

---

## 3. Component Selection

### 3.1 Bill of Materials (TC6 Option 4 FV Configuration)

| Component | Part Number | Qty | Unit Cost | Total | Notes |
|-----------|-------------|-----|-----------|-------|-------|
| BR (Barlow Ridge) | TBD | 1 | $20.00 | $20.00 | TBT4 Controller |
| KR (Kite Ridge) | TBD | 1 | $10.00 | $10.00 | USB4 Controller |
| FX20 | Cypress FX20 | 1 | $60.00 | $60.00 | USB Traffic Gen |
| TR (Retimer) | TBD | 1 | $10.00 | $10.00 | External Retimer |
| MST Realtek | RTD2198 | 4 | $20.00 | $80.00 | DP Sink Hub |
| PD Controller | PMG1-S3 | 2 | $2.34 | $4.68 | USB-PD |
| USB2 Hub | TBD | 1 | $3.75 | $3.75 | USB2.0 Distribution |
| High-Speed Mux | TBD | 1 | $3.00 | $3.00 | Signal Routing |
| Low-Speed Mux | TBD | 1 | $2.00 | $2.00 | Control Routing |
| SSD | TBD | 1 | $300.00 | $300.00 | M.2 NVMe |
| **Total** | | | | **$493.43** | |

### 3.2 PPV vs FV Configuration Differences

| Component | PPV Config | FV Config |
|-----------|------------|-----------|
| FX20 | 2x ($120) | 1x ($60) |
| MST Realtek | 3x ($60) | 4x ($80) |
| TR Retimer | 2x ($20) | 1x ($10) |
| SSD | 2x ($600) | 1x ($300) |
| **Total** | **$844.43** | **$493.43** |

---

## 4. Interface Specifications

### 4.1 UFP (Upstream Facing Port)
- **Type**: USB Type-C receptacle
- **Protocols**: TBT4, USB4, USB3.2, DP Alt Mode
- **Power**: 5V/3A, 12V/3A (PD negotiated)

### 4.2 DFP (Downstream Facing Ports)
- **Quantity**: 2
- **Type**: USB Type-C receptacle
- **Function**: External device connection, display output

### 4.3 Backdoor Host
- **Type**: Mini-USB Type-B receptacle
- **Controller**: FTDI FT4232H
- **Protocols**: USB 2.0 HS, UART, I2C, SPI, GPIO

### 4.4 Power Input
- **Type**: Barrel jack or ATX header
- **Voltage**: 12V DC
- **Current**: TBD (max 5A estimated)

### 4.5 M.2 Socket
- **Form Factor**: M.2 2280 (2230 alternative)
- **Interface**: PCIe Gen4 x4
- **Keying**: M-key

### 4.6 DIP Switches
- **Bits**: 4 (16 values)
- **Function**: Card ID, default mode selection

---

## 5. Control Register Map

### 5.1 FTDI GPIO Allocation

| GPIO | Function | Direction | Notes |
|------|----------|-----------|-------|
| GPIO0 | HS_MUX_SEL[0] | Output | High-speed mux select |
| GPIO1 | HS_MUX_SEL[1] | Output | High-speed mux select |
| GPIO2 | HS_MUX_SEL[2] | Output | High-speed mux select |
| GPIO3 | BR_RESET_N | Output | BR reset (active low) |
| GPIO4 | KR_RESET_N | Output | KR reset (active low) |
| GPIO5 | FX20_RESET_N | Output | FX20 reset (active low) |
| GPIO6 | MST_RESET_N | Output | MST reset (active low) |
| GPIO7 | LED_CTRL | Output | Status LED control |
| GPIO8 | DIP_SW[0] | Input | DIP switch bit 0 |
| GPIO9 | DIP_SW[1] | Input | DIP switch bit 1 |
| GPIO10 | DIP_SW[2] | Input | DIP switch bit 2 |
| GPIO11 | DIP_SW[3] | Input | DIP switch bit 3 |

### 5.2 High-Speed Mux Select

| SEL[2:0] | Path |
|----------|------|
| 000 | UFP → BR (TBT/USB4 Tunnel) |
| 001 | UFP → KR (USB4 Native) |
| 010 | UFP → FX20 (USB Native Direct) |
| 011 | UFP → DFP1 (Pass-through) |
| 100 | UFP → DFP2 (Pass-through) |
| 101-111 | Reserved |

---

## 6. Mode Definitions

### 6.1 Operating Modes

| Mode ID | Name | Description | Mux Path |
|---------|------|-------------|----------|
| 0x00 | TBT3_TUNNEL | TBT3 PCIe/DP/USB tunnel | UFP→BR |
| 0x01 | TBT4_TUNNEL | TBT4 PCIe/DP/USB tunnel | UFP→BR |
| 0x02 | USB4_TUNNEL | USB4 tunneling mode | UFP→BR |
| 0x03 | USB4_NATIVE | USB4 native via KR | UFP→KR |
| 0x04 | USB3_NATIVE | USB3.2 direct to FX20 | UFP→FX20 |
| 0x05 | DP_ALT | DisplayPort Alt Mode | UFP→BR→MST |
| 0x06 | MFD | Multi-Function Device | UFP→BR |
| 0x07 | PASSTHROUGH | Direct DFP connection | UFP→DFP |
| 0x08 | DISCONNECTED | No device attached | - |

### 6.2 Sub-Modes for USB Native

| Sub-Mode | Speed | Width |
|----------|-------|-------|
| GEN1X1 | 5 Gbps | x1 |
| GEN1X2 | 5 Gbps | x2 |
| GEN2X1 | 10 Gbps | x1 |
| GEN2X2 | 20 Gbps | x2 |

---

## 7. Firmware Architecture

### 7.1 Firmware Components

| Component | Type | Programming | Notes |
|-----------|------|-------------|-------|
| BR FW | TBT Controller | SPI via TenLira/UFP | External EEPROM |
| KR FW | USB4 Controller | SPI via FTDI | External EEPROM |
| FX20 FW | USB EP | I2C/SPI via FTDI | Internal Flash |
| PD FW | PMG1-S3 | SPI via EzProg | Integrated |
| MST FW | Realtek | I2C via FTDI | Internal ROM |
| BLT EEPROM | Config | I2C via FTDI | Build info, S/N |

### 7.2 Default Mode Selection

```
Power On
    │
    ▼
Read DIP Switches
    │
    ▼
┌───────────────────┐
│  DIP Value        │
│  0x0: TBT3        │
│  0x1: TBT4        │
│  0x2: USB4        │
│  0x3: USB3_GEN2X2 │
│  0x4: USB3_GEN1X1 │
│  0x5: DP_ALT      │
│  0x6: MFD         │
│  0x7: PASSTHROUGH │
│  0x8-0xF: Reserved│
└───────────────────┘
    │
    ▼
Configure Mux & Components
    │
    ▼
Ready for Operation
```

---

## 8. Mechanical Specifications

### 8.1 Form Factor
- **Target Size**: Same as ThunderCat3.0 (best effort)
- **Max Height**: ATX power connector height (primary side)
- **Secondary Side**: No components

### 8.2 Mounting
- **Holes**: Same positions as ThunderCat3.0
- **Bracket**: Reuse existing brackets

### 8.3 Connectors
- **UFP**: USB Type-C (front edge)
- **DFP x2**: USB Type-C (front edge)
- **Backdoor**: Mini-USB (same location as TC4/TC5)
- **M.2**: Same location as previous TCs
- **Power**: 12V barrel jack or ATX

---

## 9. Test Points & Debug

### 9.1 Status LEDs

| LED | Color | Function |
|-----|-------|----------|
| PWR | Green | Power good |
| TBT | Blue | TBT/USB4 link up |
| USB | Blue | USB3 active |
| DP | Blue | DP link up |
| PCIe | Blue | PCIe link up |
| ERR | Red | Error condition |
| RST | Yellow | Reset active |

### 9.2 Test Points
- SPI bus signals
- I2C bus signals
- Reset signals
- Power rails (12V, 5V, 3.3V, 1.8V)

---

## 10. Action Items & Open Issues

| ID | Item | Owner | Priority | Status |
|----|------|-------|----------|--------|
| 1 | PD rate control exploration | Oded.D/Shay | High | Open |
| 2 | External retimer selection | HW Team | High | Open |
| 3 | TBT3 vs UHBR13.5 priority | Martin/Naod | Medium | Open |
| 4 | PCIe hotplug clarification | CCD Team | Medium | Open |
| 5 | On-board HDMI/DP exploration | HW Team | Low | Open |
| 6 | FX20 detailed specifications | SW Team | High | Open |
| 7 | MST SST mode FW development | Realtek | High | Open |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| 0.1 | 2026-05-25 | AI Assistant | Initial draft |
