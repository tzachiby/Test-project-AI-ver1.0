# ThunderCat6 Gen T (PCIe Tunneling) Requirements

## Document Control
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-05-30 | - | Placeholder |

---

## Overview

Gen T refers to PCIe Tunneling capability through USB4/Thunderbolt connection.
TC6 must validate PCIe tunnel establishment to internal M.2 NVMe SSD.

---

## TODO: Required Information

- [ ] BR datasheet - PCIe tunnel configuration
- [ ] USB4 specification - tunnel protocol details
- [ ] M.2 SSD requirements

---

## Test Requirements (From TC6 Requirements)

| Requirement | TC6 Support |
|-------------|-------------|
| x4 PCIe Gen4 Tunneled (M.2 SSD) | Yes |
| PCIe Hot plug | Yes |

---

## Test Scenarios

**TODO: Define after obtaining BR datasheet**

1. PCIe tunnel establishment
2. SSD enumeration
3. Bandwidth validation
4. Hot plug testing
5. Mixed tunnels (PCIe + DP)

---

## Implementation Details

**TODO: From BR datasheet**

- Tunnel configuration: **TODO**
- Bandwidth allocation: **TODO**
- Hot plug handling: **TODO**

---

## Next Steps

1. Obtain BR PCIe tunnel documentation
2. Define test scenarios
3. Create validation plan
