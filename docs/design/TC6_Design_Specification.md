# ThunderCat6 Design Specification

## Document Control
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-05-30 | - | Placeholder - awaiting datasheets |

---

## TODO: Required Information

- [ ] IC datasheets for all components
- [ ] Mechanical requirements
- [ ] Thermal requirements
- [ ] Reference designs (if available)

---

## Design Goals (From TC6 Requirements)

### TC5 Showstoppers to Address

1. **BR + USB = No Data** - Need bypass path
   - Solution: **TODO: Define after obtaining BR datasheet**

2. **FX3 No LPM Support** - Replace with FX20
   - Solution: FX20 selected (from requirements)
   - Implementation: **TODO: From FX20 datasheet**

3. **Mode Switch > 7 seconds** - Target < 0.5 seconds
   - Solution: **TODO: Define switching architecture**

### New Requirements

- USB3 Native Speed Downgrade (Gen1x1, Gen1x2, Gen2x1, Gen2x2)
- Full TCPC orientation support
- Gen T (PCIe Tunneling) validation
- DP SST mode support

---

## Component Selection

| Component | Selected | Rationale | Datasheet |
|-----------|----------|-----------|-----------|
| TBT4 Controller | BR (Barlow Ridge) | From requirements | **TODO** |
| USB4 Controller | KR (Kite Ridge) | From requirements | **TODO** |
| USB Traffic Gen | FX20 | Replaces FX3, has LPM | **TODO** |
| PD Controller | PMG1-S3 | From requirements | Available |
| MST Hub | RTD2198 | From requirements | **TODO** |

---

## Cost Summary (From TC6 Requirements)

| Config | Total Cost |
|--------|------------|
| TC6 FV | $493.43 |
| TC6 PPV | $844.43 |
| TC5 Reference | $704.56 |

---

## Design Details

**TODO: Populate after obtaining datasheets**

### Signal Routing
- **TODO**

### Power Architecture
- **TODO**

### Control Interface
- **TODO**

---

## Next Steps

1. Obtain all IC datasheets
2. Create detailed signal routing design
3. Design power distribution
4. Define control interface
5. Create schematic
6. PCB layout
