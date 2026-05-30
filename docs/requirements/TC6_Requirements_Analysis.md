# ThunderCat6 Requirements Analysis

## Document Control
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-05-25 | AI Assistant | Initial draft based on TC6 requirements |

---

## 1. Executive Summary

ThunderCat6 (TC6) is the next generation test card designed to address limitations identified in TC5 while supporting new platform validation requirements. This document analyzes the TC6 requirements and compares them with TC5 capabilities.

---

## 2. Requirements Summary

### 2.1 Supported Tunnel Modes

| Requirement | TC5 PPV | TC5 FV | TC6 PPV | TC6 FV | Notes |
|-------------|---------|--------|---------|--------|-------|
| x4 PCIe Gen4 Tunneled (M.2 SSD) | Yes | Yes | Yes | Yes | |
| DP2.0 Tunneled (DPCD device) | Yes | Yes | Yes | Yes | |
| USB3.2x2 Tunneled (MSD) | Yes | Yes | Yes | Yes | |
| MFDP Tunneled | No | No | No | No | Not supported |
| USB Hot plug (MSD reset) | Yes | Yes | Yes | Yes | |
| DP Hot plug (HPD) | Yes | Yes | Yes | Yes | |

### 2.2 Supported Alt Modes

| Requirement | TC5 PPV | TC5 FV | TC6 PPV | TC6 FV | Notes |
|-------------|---------|--------|---------|--------|-------|
| DP2.0/DP2.1 Alt mode | Yes | Yes | Yes | Yes | |
| USB3.2x1 Native Mode | No | TBD | No | **Yes** | ✅ NEW in TC6 |
| USB3.2x2 Native Mode | Yes | Yes | Yes | Yes | |

### 2.3 USB Protocol Support

| Requirement | TC5 PPV | TC5 FV | TC6 PPV | TC6 FV | Notes |
|-------------|---------|--------|---------|--------|-------|
| USB Bulk | Yes | Yes | Yes | Yes | |
| USB Interrupt | Yes | Yes | Yes | Yes | |
| USB Isoc In | Yes | Yes | Yes | Yes | |
| USB Isoc Out | Yes | Yes | Yes | Yes | |
| All lane/port configs | No | TBD | No | **Yes** | ✅ NEW: Gen1X1, Gen1X2, Gen2X1, Gen2X2 |

### 2.4 Multi-Function Mode

| Requirement | TC5 PPV | TC5 FV | TC6 PPV | TC6 FV | Notes |
|-------------|---------|--------|---------|--------|-------|
| MF mode (USB3.2x1 & DP2.0 x2) | Yes | Yes | Yes | Yes | |
| MFD Hot plug | Yes | Yes | Yes | Yes | |

### 2.5 Special Modes

| Requirement | TC5 PPV | TC5 FV | TC6 PPV | TC6 FV | Notes |
|-------------|---------|--------|---------|--------|-------|
| Empty Dongle (No connect) | No | Reject | No | **Yes** | ✅ NEW in TC6 |
| NDA (BR/KR disconnected) | No | TBD | No | **Yes** | ✅ NEW in TC6 |

### 2.6 USB2.0 Support

| Requirement | TC5 PPV | TC5 FV | TC6 PPV | TC6 FV | Notes |
|-------------|---------|--------|---------|--------|-------|
| USB2 MSD/connector | Yes | Yes | Yes | Yes | |
| USB2.0 controller selection | Yes | Yes | Yes | Yes | UFP or BR (TBT3 mode) |

### 2.7 Orientation Support

| Requirement | TC5 PPV | TC5 FV | TC6 PPV | TC6 FV | Notes |
|-------------|---------|--------|---------|--------|-------|
| USB orientation change | No | No | No | No | |
| Full TCPC orientation | Reject | Reject | Yes | Yes | ✅ NEW in TC6 |

### 2.8 Mode Switching Performance

| Requirement | TC5 PPV | TC5 FV | TC6 PPV | TC6 FV | Notes |
|-------------|---------|--------|---------|--------|-------|
| Mode switch < 7 seconds | Yes | Yes | Yes | Yes | |
| Mode switch < 0.5 seconds | Best Effort | Best Effort | **Yes** | **Yes** | ✅ IMPROVED |
| No platform reset required | Yes | Yes | Yes | Yes | |
| Switch with power On/Off | TBD | TBD | Yes | Yes | ✅ IMPROVED |

### 2.9 Port Identification & Diagnostics

| Requirement | TC5 PPV | TC5 FV | TC6 PPV | TC6 FV | Notes |
|-------------|---------|--------|---------|--------|-------|
| DIP switches (16 values) | Yes | Yes | Yes | Yes | 4 bits |
| DIP value to BR scratchpad | TBD | TBD | Yes | Yes | ✅ IMPROVED |
| Serial number | Yes | Yes | Yes | Yes | Like Cswitch |
| Critical signals to LED | Partial | Partial | Yes | Yes | ✅ IMPROVED |
| Endpoint info readback | Reject | Yes | Yes | Yes | |
| Recovery mode | Reject | Reject | Yes | Yes | ✅ NEW |

### 2.10 Programming Support

| Requirement | TC5 PPV | TC5 FV | TC6 PPV | TC6 FV | Notes |
|-------------|---------|--------|---------|--------|-------|
| BLT via inline | Yes | Yes | Yes | Yes | |
| Offline DMC programming | Yes | Yes | Yes | Yes | |
| TBT4 SPI programming | Reject | Reject | Yes | Yes | ✅ NEW |
| Independent boot | Reject | Reject | Yes | Yes | ✅ NEW |
| SSD programming via backdoor | NTH | Best Effort | NTH | **Yes** | ✅ IMPROVED |

---

## 3. TC5 Feedback Analysis (Issues to Address in TC6)

### 3.1 Showstopper Issues

| # | Issue | TC6 Solution | Priority |
|---|-------|--------------|----------|
| 1 | Native USB speed downgrade not supported via BR | External high-speed mux with FX20 direct to UFP | Showstopper |
| 2 | MFD USB/DP rate downgrade not controllable | PD control exploration + external mux | Showstopper |
| 3 | Variable LTTPR configuration not supported | External retimers (max options TBD) | Showstopper |
| 4 | DP SST limited (1 display in MST config) | Realtek FW update for true SST mode | Showstopper |
| 5 | USB4v1 Gen3/Gen2 downgrade not supported | PD control + cable lane support | Showstopper |

### 3.2 High Priority Issues

| # | Issue | TC6 Solution | Priority |
|---|-------|--------------|----------|
| 6 | No BR bypass for commercial devices | Add DFP-UFP direct connection options | High |
| 7 | Hotplug/switch time > 1 second | HW optimization target | High |
| 8 | FX chip lacks LPM support | FX20 supports U1/U2/U3 + Deep Sleep | High |
| 9 | Native HDMI/DP module switching | Explore on-board HDMI/DP connectivity | High |

### 3.3 Medium Priority Issues

| # | Issue | TC6 Solution | Priority |
|---|-------|--------------|----------|
| 10 | Cannot disconnect DFP without cswitch | Add direct connection control | Medium |
| 11 | Multiple UFP identification limited | Add Mux select indication to FTDI | Medium |
| 12 | PCIe hotplug behind TBT not functional | Clarification needed from CCD | Medium |
| 13 | Only 2 displays supported | Explore mux to BR DFP for 3 sinks | Medium |
| 14 | No power on/off switch | Add on/off power switch | Medium |

---

## 4. Component Selection (Cost Analysis)

### 4.1 TC6 Option 4 (Recommended) vs TC5

| Component | TC5 Cost | TC6 PPV | TC6 FV | Notes |
|-----------|----------|---------|--------|-------|
| BR (Barlow Ridge) | $20 | $20 | $20 | Same |
| FX3 | $18.72 | - | - | Replaced by FX20 |
| FX20 | - | $120 | $60 | **New** - Better LPM |
| MST Realtek | $20 | $60 | $80 | More displays |
| PD | $2.34 | $4.68 | $4.68 | Dual PD |
| USB2 Hub | $2.50 | $3.75 | $3.75 | Enhanced |
| High Speed Mux | $3 | $4 | $3 | For bypass |
| KR (Kite Ridge) | - | $10 | $10 | **New** |
| TR (Retimer) | - | $20 | $10 | **New** |
| Low Speed Mux | - | $2 | $2 | **New** |
| SSD | $300 | $600 | $300 | Higher for PPV |
| ASMedia | $8 | - | - | Removed |
| Phison | $330 | - | - | Removed |
| **Total** | **$704.56** | **$844.43** | **$493.43** | |

### 4.2 Cost Analysis Summary
- TC6 FV is **30% cheaper** than TC5 ($493 vs $705)
- TC6 PPV is **20% more expensive** due to additional components for full validation

---

## 5. Architecture Implications

### 5.1 Block Diagram Changes

**New Connections Required:**
1. **UFP → High-Speed Mux → FX20** (Direct USB path, bypassing BR)
2. **UFP → High-Speed Mux → DFP** (Direct external device connection)
3. **KR integration** alongside BR for USB4 support
4. **External Retimer** connections for LTTPR testing

### 5.2 Control Interfaces

| Interface | TC5 | TC6 |
|-----------|-----|-----|
| FTDI Backdoor | ✓ | ✓ |
| PD Control | Basic | **Enhanced** (rate control) |
| BR Register | ✓ | ✓ |
| KR Register | - | **New** |
| High-Speed Mux | - | **New** (I2C/GPIO) |

---

## 6. Open Items & Action Required

| Item | Owner | Due Date | Status |
|------|-------|----------|--------|
| PD control exploration for rate downgrade | Oded.D/Shay | TBD | Open |
| External retimer options | HW Team | TBD | Open |
| TBT3 vs UHBR13.5 priority decision | Martin/Naod | TBD | Open |
| PCIe hotplug clarification | CCD Team | TBD | Open |
| On-board HDMI/DP connectivity | HW Team | TBD | Open |

---

## 7. Appendix

### 7.1 Reference Documents
- ThunderCat6p0_Requirements_rev0p1FOR TEST CARD AI.xlsx
- ThunderCat5p0_Requirements_rev0p1.xlsx
- ThunderCat5_Architecture_Rev13_High_Level_FAB_C.pdf

### 7.2 Glossary
- **BR**: Barlow Ridge (Thunderbolt 4 Controller)
- **KR**: Kite Ridge (USB4 Controller)
- **FX20**: USB Synthetic Traffic Generator (replaces FX3)
- **LTTPR**: Link Training Tunable PHY Repeater
- **MFD**: Multi-Function Device
- **DPCD**: DisplayPort Configuration Data
- **HPD**: Hot Plug Detect
- **MST**: Multi-Stream Transport
- **SST**: Single-Stream Transport
