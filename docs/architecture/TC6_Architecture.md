# ThunderCat6 System Architecture

## Document Control
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-05-30 | - | Placeholder - awaiting datasheets |

---

## TODO: Required Information

- [ ] IC datasheets for interface definitions
- [ ] Signal routing requirements
- [ ] Power architecture

---

## High-Level Block Diagram (From Requirements)

```
┌─────────────────────────────────────────────────────────┐
│                    ThunderCat6                          │
│                                                         │
│  UFP ──► [Routing] ──► BR ──► SSD (PCIe)               │
│              │             └──► MST (DP)                │
│              │             └──► USB3                    │
│              │                                          │
│              ├──► KR (USB4)                            │
│              │                                          │
│              └──► FX20 (USB Traffic)                   │
│                                                         │
│  PD x2 ◄──► CC Control                                 │
│                                                         │
│  Backdoor ◄──► Control Interface                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Components (From TC6 Requirements)

| Component | Function | Datasheet Status |
|-----------|----------|------------------|
| BR (Barlow Ridge) | TBT4 Controller | **TODO: Obtain** |
| KR (Kite Ridge) | USB4 Controller | **TODO: Obtain** |
| FX20 | USB Traffic Generator | **TODO: Obtain** |
| PMG1-S3 x2 | USB-PD Controllers | Available from Infineon |
| MST Realtek | DP Sink Hub | **TODO: Obtain** |

---

## Supported Modes (From TC6 Requirements)

| Mode | Description |
|------|-------------|
| TBT4 Tunnel | PCIe + DP + USB through BR |
| USB4 Tunnel | USB4 native mode |
| USB3 Native | Gen1x1, Gen1x2, Gen2x1, Gen2x2 |
| DP Alt Mode | DP2.0/2.1 |
| MFD | Multi-Function Device |

---

## Interface Details

**TODO: Populate after obtaining datasheets**

### Signal Interfaces
- UFP to BR: **TODO**
- UFP to KR: **TODO**
- UFP to FX20: **TODO**
- BR to SSD: **TODO**
- BR to MST: **TODO**

### Control Interfaces
- Backdoor type: **TODO**
- I2C topology: **TODO**

---

## Next Steps

1. Obtain IC datasheets
2. Define signal routing architecture
3. Define control architecture
4. Create detailed block diagram
5. Design power distribution
