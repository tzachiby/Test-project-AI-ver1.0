# ThunderCat6 Bill of Materials (BOM)

## Document Control
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-05-30 | AI Assistant | Initial BOM based on TC6 requirements |

---

## 1. BOM Summary

| Configuration | Total Cost | Notes |
|---------------|------------|-------|
| **TC6 PPV** | $844.43 | Full validation, dual components |
| **TC6 FV** | $493.43 | Production validation |
| **TC5 Reference** | $704.56 | Previous generation |

---

## 2. Main Controllers

| Item | Part Number | Description | Qty PPV | Qty FV | Unit Cost | PPV Total | FV Total | Supplier |
|------|-------------|-------------|---------|--------|-----------|-----------|----------|----------|
| U1 | BR-TBD | Barlow Ridge TBT4 Controller | 1 | 1 | $20.00 | $20.00 | $20.00 | Intel |
| U2 | KR-TBD | Kite Ridge USB4 Controller | 1 | 1 | $10.00 | $10.00 | $10.00 | Intel |
| U3 | CYUSB4356 | FX20 USB Traffic Generator | 2 | 1 | $60.00 | $120.00 | $60.00 | Cypress/Infineon |
| U4 | RTD2198 | Realtek MST Hub (DP Sink) | 3 | 4 | $20.00 | $60.00 | $80.00 | Realtek |

---

## 3. Power Delivery & Control

| Item | Part Number | Description | Qty PPV | Qty FV | Unit Cost | PPV Total | FV Total | Supplier |
|------|-------------|-------------|---------|--------|-----------|-----------|----------|----------|
| U5 | PMG1-S3 | USB-PD Controller | 2 | 2 | $2.34 | $4.68 | $4.68 | Infineon |
| U6 | TBD | USB2.0 Hub Controller | 1 | 1 | $3.75 | $3.75 | $3.75 | TBD |
| U7 | FT4232H | FTDI USB-UART/GPIO | 1 | 1 | $5.00 | $5.00 | $5.00 | FTDI |

---

## 4. Signal Routing

| Item | Part Number | Description | Qty PPV | Qty FV | Unit Cost | PPV Total | FV Total | Supplier |
|------|-------------|-------------|---------|--------|-----------|-----------|----------|----------|
| U8 | PI3USB30532 | High-Speed USB3.2 Mux | 2 | 1 | $3.00 | $6.00 | $3.00 | Diodes Inc |
| U9 | TBD | Low-Speed Control Mux | 1 | 1 | $2.00 | $2.00 | $2.00 | TI |
| U10 | DS100BR410 | USB4 Retimer | 2 | 1 | $10.00 | $20.00 | $10.00 | TI |

---

## 5. Storage

| Item | Part Number | Description | Qty PPV | Qty FV | Unit Cost | PPV Total | FV Total | Supplier |
|------|-------------|-------------|---------|--------|-----------|-----------|----------|----------|
| SSD1 | TBD | M.2 NVMe SSD (Gen4 x4) | 2 | 1 | $300.00 | $600.00 | $300.00 | Samsung/WD |

---

## 6. Connectors

| Item | Part Number | Description | Qty | Unit Cost | Total | Supplier |
|------|-------------|-------------|-----|-----------|-------|----------|
| J1 | USB4125-GF-A | USB Type-C (UFP) | 1 | $2.50 | $2.50 | GCT |
| J2 | USB4125-GF-A | USB Type-C (DFP1) | 1 | $2.50 | $2.50 | GCT |
| J3 | USB4125-GF-A | USB Type-C (DFP2) | 1 | $2.50 | $2.50 | GCT |
| J4 | 10118193-0001LF | Mini-USB Type-B (Backdoor) | 1 | $0.80 | $0.80 | Amphenol |
| J5 | 2199230-4 | M.2 Socket (Key-M, 2280) | 1 | $3.00 | $3.00 | TE Connectivity |
| J6 | PJ-102AH | DC Barrel Jack (12V) | 1 | $0.50 | $0.50 | CUI |

---

## 7. Power Regulation

| Item | Part Number | Description | Qty | Unit Cost | Total | Supplier |
|------|-------------|-------------|-----|-----------|-------|----------|
| VR1 | TPS62912 | 12V to 5V Step-Down (3A) | 1 | $2.00 | $2.00 | TI |
| VR2 | TPS62913 | 5V to 3.3V Step-Down (2A) | 1 | $1.80 | $1.80 | TI |
| VR3 | TPS62160 | 3.3V to 1.8V Step-Down (1A) | 1 | $1.50 | $1.50 | TI |
| VR4 | TPS62162 | 3.3V to 1.1V Step-Down (1A) | 1 | $1.50 | $1.50 | TI |

---

## 8. Passive Components (Summary)

| Category | Est. Qty | Est. Cost |
|----------|----------|-----------|
| Resistors (0402/0603) | ~200 | $5.00 |
| Capacitors (0402/0603/0805) | ~150 | $8.00 |
| Inductors | ~10 | $3.00 |
| Ferrite Beads | ~20 | $2.00 |
| ESD Protection | ~10 | $5.00 |
| Crystals/Oscillators | ~3 | $4.00 |
| **Subtotal** | | **$27.00** |

---

## 9. Mechanical & Debug

| Item | Part Number | Description | Qty | Unit Cost | Total |
|------|-------------|-------------|-----|-----------|-------|
| SW1 | CTS 219-4MST | DIP Switch 4-bit | 1 | $0.50 | $0.50 |
| LED1-7 | LTST-C171 | Status LEDs (Various colors) | 7 | $0.10 | $0.70 |
| TP1-20 | 5019 | Test Points | 20 | $0.05 | $1.00 |
| HDR1 | TSW-110-07-G-S | Programming Header 10-pin | 2 | $0.80 | $1.60 |

---

## 10. PCB

| Item | Description | Cost |
|------|-------------|------|
| PCB | 6-layer, 100x80mm, ENIG, controlled impedance | $50.00 (prototype qty 10) |

---

## 11. Total Cost Summary

### PPV Configuration
| Category | Cost |
|----------|------|
| Main Controllers | $210.00 |
| Power & Control | $13.43 |
| Signal Routing | $28.00 |
| Storage | $600.00 |
| Connectors | $11.80 |
| Power Regulation | $6.80 |
| Passives | $27.00 |
| Mechanical & Debug | $3.80 |
| PCB | $5.00 |
| **Total PPV** | **~$906** |

### FV Configuration
| Category | Cost |
|----------|------|
| Main Controllers | $170.00 |
| Power & Control | $13.43 |
| Signal Routing | $15.00 |
| Storage | $300.00 |
| Connectors | $11.80 |
| Power Regulation | $6.80 |
| Passives | $27.00 |
| Mechanical & Debug | $3.80 |
| PCB | $5.00 |
| **Total FV** | **~$553** |

---

## 12. Approved Vendors List (AVL)

| Component Type | Primary | Alternate |
|----------------|---------|-----------|
| TBT Controller | Intel | - |
| USB4 Controller | Intel | - |
| FX20 | Infineon/Cypress | - |
| MST Hub | Realtek | - |
| PD Controller | Infineon | - |
| USB Hub | TBD | Microchip |
| FTDI | FTDI | - |
| High-Speed Mux | Diodes Inc | TI |
| Retimer | TI | Parade |
| SSD | Samsung | WD/SK Hynix |
| Connectors | GCT/Amphenol | JAE |
| Power Regulators | TI | MPS |

---

## 13. Long Lead Time Items

| Item | Lead Time | Action |
|------|-----------|--------|
| Barlow Ridge | 12 weeks | Order early |
| Kite Ridge | 12 weeks | Order early |
| FX20 | 16 weeks | Order immediately |
| RTD2198 | 10 weeks | Confirm availability |
| M.2 SSD | 4 weeks | Standard |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| 0.1 | 2026-05-30 | AI | Initial BOM |
