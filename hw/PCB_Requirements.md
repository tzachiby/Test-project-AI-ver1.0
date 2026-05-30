# ThunderCat6 PCB Design Requirements

## 1. General Specifications

| Parameter | Specification |
|-----------|---------------|
| **Form Factor** | ThunderCat3.0 Compatible |
| **Dimensions** | 100mm x 80mm (±0.5mm) |
| **Layer Count** | 6 layers minimum |
| **Thickness** | 1.6mm ±10% |
| **Material** | FR-4, Tg ≥ 170°C |
| **Surface Finish** | ENIG (Electroless Nickel Immersion Gold) |
| **Copper Weight** | 1 oz outer, 0.5 oz inner |
| **Min Trace/Space** | 3.5 mil / 3.5 mil |
| **Min Via** | 8 mil drill, 14 mil pad |
| **Impedance Control** | Yes (±10%) |

---

## 2. Layer Stackup

```
Layer 1 (TOP)     ─── Signal (Components, HS routing)    35µm Cu
─────────────────────────────────────────────────────── Prepreg 100µm
Layer 2 (GND1)    ─── Ground Plane (Reference)          18µm Cu
─────────────────────────────────────────────────────── Core 200µm
Layer 3 (SIG1)    ─── Signal (Internal routing)         18µm Cu
─────────────────────────────────────────────────────── Prepreg 360µm
Layer 4 (PWR)     ─── Power Planes (Split)              18µm Cu
─────────────────────────────────────────────────────── Core 200µm
Layer 5 (GND2)    ─── Ground Plane (Reference)          18µm Cu
─────────────────────────────────────────────────────── Prepreg 100µm
Layer 6 (BOT)     ─── Signal (Components, HS routing)   35µm Cu
```

---

## 3. High-Speed Signal Requirements

### 3.1 USB4/Thunderbolt Differential Pairs

| Parameter | Requirement |
|-----------|-------------|
| **Differential Impedance** | 85Ω ±10% |
| **Single-Ended Impedance** | 50Ω ±10% |
| **Trace Width** | 4 mil (calculated) |
| **Spacing** | 4 mil (pair-to-pair: 20 mil min) |
| **Max Length Mismatch** | ±2 mil intra-pair, ±50 mil inter-lane |
| **Via Stubs** | Back-drilled or HDI microvias |
| **Reference Plane** | GND (continuous under HS traces) |

### 3.2 USB 3.2 Differential Pairs

| Parameter | Requirement |
|-----------|-------------|
| **Differential Impedance** | 90Ω ±10% |
| **Trace Width** | 5 mil (calculated) |
| **Max Length Mismatch** | ±5 mil intra-pair |

### 3.3 USB 2.0 Differential Pairs

| Parameter | Requirement |
|-----------|-------------|
| **Differential Impedance** | 90Ω ±10% |
| **Trace Width** | 8 mil |
| **Length Matching** | Not critical |

### 3.4 PCIe Gen4 x4 (to M.2 SSD)

| Parameter | Requirement |
|-----------|-------------|
| **Differential Impedance** | 85Ω ±7% |
| **Trace Width** | 4 mil |
| **Max Trace Length** | 6 inches |
| **Lane-to-Lane Skew** | ±10 mil |

---

## 4. Power Distribution

### 4.1 Power Rails
| Rail | Current | Plane/Polygon Width |
|------|---------|---------------------|
| 12V | 3A | 100 mil polygon |
| 5V | 2A | 80 mil polygon |
| 3.3V | 1.5A | 60 mil polygon |
| 1.8V | 500mA | 40 mil polygon |
| 1.1V | 500mA | 40 mil polygon |

### 4.2 Decoupling Requirements
- **Per IC**: 100nF ceramic + 10µF ceramic
- **Power Entry**: 100µF bulk + 10µF ceramic array
- **High-Frequency**: 1nF near high-speed I/O
- **Placement**: Within 50 mil of power pins

---

## 5. Component Placement Guidelines

### 5.1 Critical Placement Rules
1. **BR (U1)**: Center of board, direct path to UFP connector
2. **HS Mux (U8)**: Between UFP and BR, minimize trace length
3. **FX20 (U3)**: Near HS mux for direct USB path
4. **Type-C (J1-J3)**: Edge-mounted, standard orientation
5. **M.2 (J5)**: Bottom layer, away from heat sources
6. **FTDI (U7)**: Near Mini-USB, away from HS signals

### 5.2 Thermal Considerations
| Component | Thermal Pad | Via Array |
|-----------|-------------|-----------|
| BR (U1) | Yes | 16x (8 mil) |
| KR (U2) | Yes | 12x (8 mil) |
| FX20 (U3) | Yes | 9x (8 mil) |
| Power Regulators | Yes | 4x each |

---

## 6. Signal Integrity Requirements

### 6.1 Crosstalk
- **Aggressor-to-Victim**: 3x trace width minimum spacing
- **HS to LS signals**: 50 mil minimum clearance
- **Clock to Data**: 30 mil minimum clearance

### 6.2 Return Path
- **All HS signals**: Reference to GND plane
- **No plane splits**: Under high-speed routing
- **Via stitching**: Every 200 mil along board edges

### 6.3 Length Matching Groups
| Group | Max Skew |
|-------|----------|
| USB4 Lane 0 (TX/RX) | ±2 mil |
| USB4 Lane 1 (TX/RX) | ±2 mil |
| USB4 Lane 2 (TX/RX) | ±2 mil |
| USB4 Lane 3 (TX/RX) | ±2 mil |
| Inter-lane (all USB4) | ±50 mil |
| PCIe Gen4 intra-pair | ±2 mil |
| PCIe Gen4 inter-lane | ±10 mil |

---

## 7. Connector Footprints

### 7.1 Type-C (UFP/DFP)
- **Footprint**: USB4125-GF-A (GCT)
- **Shield Tie**: Multiple vias to GND
- **Mounting**: Through-hole reinforced

### 7.2 Mini-USB (Backdoor)
- **Footprint**: 10118193-0001LF
- **ESD Protection**: TVS on D+/D-

### 7.3 M.2 Socket
- **Footprint**: 2199230-4 (TE)
- **Orientation**: Card extends toward board center
- **Standoff**: 2.3mm (for M.2 2280)

### 7.4 DC Jack
- **Footprint**: PJ-102AH
- **Routing**: Wide traces direct to bulk caps

---

## 8. Manufacturing Notes

### 8.1 Silkscreen
- Component designators (U, R, C, J, etc.)
- Polarity markers for capacitors/connectors
- Pin 1 indicators
- Test point labels
- Version and date code area
- Intel logo area (if required)

### 8.2 Solder Mask
- **Color**: Green (standard) or Black
- **Opening**: Mask-defined for BGA/QFN
- **Dam**: Between fine-pitch pads

### 8.3 Assembly Notes
- **All SMT**: Single reflow (TOP priority)
- **PTH connectors**: Wave/hand solder
- **QFN/BGA**: X-ray inspection required
- **AOI**: 100% inspection

---

## 9. Test Points

| TP# | Signal | Purpose |
|-----|--------|---------|
| TP1 | GND | Ground reference |
| TP2 | 12V | Power input |
| TP3 | 5V | 5V rail |
| TP4 | 3.3V | 3.3V rail |
| TP5 | 1.8V | 1.8V rail |
| TP6 | 1.1V | 1.1V rail |
| TP7 | CC1 | Type-C CC1 |
| TP8 | CC2 | Type-C CC2 |
| TP9 | VBUS | Type-C VBUS |
| TP10 | SDA | I2C Data |
| TP11 | SCL | I2C Clock |
| TP12 | BR_RST | BR Reset |
| TP13 | FX20_RST | FX20 Reset |
| TP14 | MUX_SEL0 | Mux Select 0 |
| TP15 | MUX_SEL1 | Mux Select 1 |
| TP16-20 | Reserved | Future |

---

## 10. Design Review Checklist

- [ ] Layer stackup impedance calculated
- [ ] All HS pairs length matched
- [ ] No GND plane splits under HS routing
- [ ] Decoupling caps placed per guidelines
- [ ] Thermal vias under power components
- [ ] ESD protection on all external I/O
- [ ] Via stitching around board perimeter
- [ ] Mounting holes clearance verified
- [ ] BOM verified against schematic
- [ ] DRC clean (0 errors)
- [ ] Gerber review complete

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| 0.1 | 2026-05-30 | AI | Initial PCB requirements |
