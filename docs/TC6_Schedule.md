# ThunderCat6 Project Schedule

## Document Control
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-05-25 | AI Assistant | Initial draft |

---

## 1. Project Phases

### Phase 1: Requirements & Architecture (Weeks 1-4)
| Task | Owner | Start | End | Status |
|------|-------|-------|-----|--------|
| Requirements gathering | PM | W1 | W2 | ✅ Complete |
| TC5 feedback analysis | Arch Lead | W1 | W2 | ✅ Complete |
| Architecture definition | Arch Lead | W2 | W4 | 🔄 In Progress |
| Component selection | HW Lead | W2 | W4 | 📋 Pending |
| Cost analysis | PM | W3 | W4 | 📋 Pending |
| Architecture review | All | W4 | W4 | 📋 Pending |

### Phase 2: Detailed Design (Weeks 5-12)
| Task | Owner | Start | End | Status |
|------|-------|-------|-----|--------|
| Schematic design | HW Lead | W5 | W8 | 📋 Pending |
| PCB layout | HW Lead | W8 | W11 | 📋 Pending |
| FW architecture | SW Lead | W5 | W7 | 📋 Pending |
| API design | SW Lead | W6 | W8 | 📋 Pending |
| Design review | All | W12 | W12 | 📋 Pending |

### Phase 3: Prototype Build (Weeks 13-18)
| Task | Owner | Start | End | Status |
|------|-------|-------|-----|--------|
| PCB fabrication | HW Lead | W13 | W15 | 📋 Pending |
| Component procurement | PM | W13 | W14 | 📋 Pending |
| Board assembly | HW Lead | W15 | W16 | 📋 Pending |
| Initial bring-up | HW/SW | W16 | W18 | 📋 Pending |

### Phase 4: Firmware & Software (Weeks 13-22)
| Task | Owner | Start | End | Status |
|------|-------|-------|-----|--------|
| FTDI FW development | SW Lead | W13 | W18 | 📋 Pending |
| FX20 integration | SW Lead | W14 | W19 | 📋 Pending |
| PD control FW | SW Lead | W15 | W20 | 📋 Pending |
| Host API development | SW Lead | W16 | W21 | 📋 Pending |
| Test scripts | SW Lead | W18 | W22 | 📋 Pending |

### Phase 5: Validation (Weeks 19-26)
| Task | Owner | Start | End | Status |
|------|-------|-------|-----|--------|
| HW validation | HW Lead | W19 | W22 | 📋 Pending |
| FW validation | SW Lead | W20 | W23 | 📋 Pending |
| System integration | All | W22 | W25 | 📋 Pending |
| PPV sign-off | All | W25 | W26 | 📋 Pending |

### Phase 6: FV Build (Weeks 27-32)
| Task | Owner | Start | End | Status |
|------|-------|-------|-----|--------|
| FV enhancements | All | W27 | W30 | 📋 Pending |
| FV validation | All | W30 | W32 | 📋 Pending |
| FV sign-off | All | W32 | W32 | 📋 Pending |

---

## 2. Milestones

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| M1: Architecture Complete | W4 | 🔄 In Progress |
| M2: Design Review Complete | W12 | 📋 Pending |
| M3: First Prototype | W16 | 📋 Pending |
| M4: PPV Bring-up Complete | W18 | 📋 Pending |
| M5: PPV Sign-off | W26 | 📋 Pending |
| M6: FV Sign-off | W32 | 📋 Pending |

---

## 3. Risk Register

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| PD control for rate downgrade not feasible | High | Medium | Early exploration, backup plan with external components |
| FX20 availability/lead time | Medium | Low | Early procurement, alternate vendor |
| KR integration complexity | Medium | Medium | Early prototyping, TBT team engagement |
| MST SST FW not available | Medium | Medium | Early engagement with Realtek |
| Form factor constraints | Low | Medium | 2230 M.2 alternative, optimize placement |

---

## 4. Dependencies

| Dependency | Required By | Owner | Status |
|------------|-------------|-------|--------|
| PD control exploration results | W4 | Oded.D/Shay | Pending |
| TBT3 vs UHBR13.5 decision | W3 | Martin/Naod | Pending |
| External retimer options | W4 | HW Team | Pending |
| PCIe hotplug clarification | W4 | CCD Team | Pending |
| FX20 datasheet/samples | W5 | Procurement | Pending |
| Realtek SST FW commitment | W6 | SW Lead | Pending |

---

## 5. Resource Allocation

| Role | Name | Allocation |
|------|------|------------|
| PM | TBD | 50% |
| Architecture Lead | TBD | 100% |
| HW Design Lead | TBD | 100% |
| SW Lead | TBD | 100% |
| PCB Engineer | TBD | 50% |
| FW Engineer | TBD | 100% |
| Validation Engineer | TBD | 50% (ramp to 100% in Phase 5) |
