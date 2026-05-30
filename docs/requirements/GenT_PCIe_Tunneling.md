# ThunderCat6 Gen T (PCIe Tunneling) Capability

## 1. Overview

**Gen T** refers to the PCIe Tunneling capability through Thunderbolt/USB4 connection.
TC6 must validate that the host can establish PCIe tunnels to access:
- Internal M.2 NVMe SSD
- Simulated external PCIe devices

---

## 2. PCIe Tunnel Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     HOST (DUT) SYSTEM                               │
│  ┌─────────────┐                                                    │
│  │ TBT/USB4    │                                                    │
│  │ Controller  │                                                    │
│  └──────┬──────┘                                                    │
└─────────┼───────────────────────────────────────────────────────────┘
          │ USB4/TBT Cable
          │ (Up to 40Gbps)
          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     ThunderCat6 (TC6)                               │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    UFP Type-C                                 │  │
│  └───────────────────────┬──────────────────────────────────────┘  │
│                          │                                          │
│                          ▼                                          │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              Barlow Ridge (BR) Controller                     │  │
│  │                                                               │  │
│  │   ┌─────────────────────────────────────────────────────┐    │  │
│  │   │           PCIe Root Port (Gen4 x4)                  │    │  │
│  │   │                                                     │    │  │
│  │   │   Lane 0 ────┐                                      │    │  │
│  │   │   Lane 1 ────┼───► PCIe Tunnel                      │    │  │
│  │   │   Lane 2 ────┤     (16GT/s per lane)                │    │  │
│  │   │   Lane 3 ────┘                                      │    │  │
│  │   │                                                     │    │  │
│  │   └──────────────────────────┬──────────────────────────┘    │  │
│  │                              │                                │  │
│  └──────────────────────────────┼────────────────────────────────┘  │
│                                 │                                    │
│                                 ▼                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │               M.2 NVMe SSD (Key-M, 2280)                      │  │
│  │                                                               │  │
│  │   • PCIe Gen4 x4 Interface                                   │  │
│  │   • Up to 7GB/s Read, 5GB/s Write                            │  │
│  │   • NVMe 1.4 Protocol                                        │  │
│  │                                                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Gen T Test Modes

### 3.1 Mode Selection (via DIP Switch or API)

| Mode | DIP Value | Description |
|------|-----------|-------------|
| **Gen T - PCIe x4** | 0x8 | Full PCIe Gen4 x4 tunnel |
| **Gen T - PCIe x2** | 0x9 | Reduced PCIe Gen4 x2 tunnel |
| **Gen T - PCIe x1** | 0xA | Minimal PCIe Gen4 x1 tunnel |
| **Gen T - Mixed** | 0xB | PCIe + DP Alt Mode combined |
| **Gen T - Bandwidth** | 0xC | PCIe bandwidth stress test |

### 3.2 Bandwidth Allocation
```
USB4 Link Bandwidth: 40Gbps (bidirectional)
├── PCIe Tunnel:     Up to 32Gbps (PCIe Gen4 x4 = 64GT/s / 2 = 32Gbps effective)
├── DP Tunnel:       Up to 32.4Gbps (HBR3 x4)
├── USB3 Tunnel:     Up to 10Gbps (Gen2)
└── USB2 Tunnel:     480Mbps
```

---

## 4. Test Scenarios

### 4.1 Basic PCIe Tunnel Establishment
```python
def test_pcie_tunnel_establish():
    """Verify PCIe tunnel is established through USB4/TBT"""
    tc6 = ThunderCat6()
    tc6.connect()
    tc6.set_mode("GEN_T_PCIE_X4")
    
    # Verify tunnel is up
    status = tc6.get_pcie_tunnel_status()
    assert status['link_up'] == True
    assert status['width'] == 4
    assert status['speed'] == 'Gen4'
    
    # Verify SSD is enumerated on host
    assert tc6.check_ssd_enumerated()
```

### 4.2 PCIe Bandwidth Test
```python
def test_pcie_bandwidth():
    """Measure PCIe tunnel bandwidth"""
    tc6 = ThunderCat6()
    tc6.connect()
    tc6.set_mode("GEN_T_BANDWIDTH")
    
    # Run sequential read/write
    results = tc6.run_ssd_benchmark(
        test_size_gb=1,
        queue_depth=32,
        num_jobs=4
    )
    
    # Verify bandwidth meets spec
    assert results['seq_read_mbps'] >= 3000   # 3GB/s minimum (limited by tunnel)
    assert results['seq_write_mbps'] >= 2500  # 2.5GB/s minimum
    assert results['iops_4k_random'] >= 500000
```

### 4.3 Hot Plug Test
```python
def test_pcie_hotplug():
    """Test PCIe tunnel hot plug/unplug"""
    tc6 = ThunderCat6()
    
    for i in range(10):
        # Connect
        tc6.connect()
        tc6.set_mode("GEN_T_PCIE_X4")
        assert tc6.check_ssd_enumerated()
        
        # Safely eject
        tc6.safe_eject_ssd()
        
        # Disconnect
        tc6.disconnect()
        time.sleep(1)
        
    # Verify no errors
    assert tc6.get_error_count() == 0
```

### 4.4 Combined Tunnel Test (PCIe + DP)
```python
def test_mixed_tunnel():
    """Test PCIe + DP tunnels simultaneously"""
    tc6 = ThunderCat6()
    tc6.connect()
    tc6.set_mode("GEN_T_MIXED")
    
    # Verify both tunnels up
    pcie_status = tc6.get_pcie_tunnel_status()
    dp_status = tc6.get_dp_tunnel_status()
    
    assert pcie_status['link_up'] == True
    assert dp_status['link_up'] == True
    
    # Run concurrent traffic
    tc6.start_dp_pattern_generator()
    results = tc6.run_ssd_benchmark(test_size_gb=1)
    
    # Both should maintain performance
    assert results['seq_read_mbps'] >= 2000  # Reduced due to sharing
    assert dp_status['no_glitch'] == True
```

### 4.5 Link Degradation Test
```python
def test_pcie_link_recovery():
    """Test PCIe tunnel recovery from errors"""
    tc6 = ThunderCat6()
    tc6.connect()
    tc6.set_mode("GEN_T_PCIE_X4")
    
    # Inject errors
    tc6.inject_link_error(count=10)
    
    # Verify recovery
    time.sleep(2)
    status = tc6.get_pcie_tunnel_status()
    assert status['link_up'] == True
    assert status['recovery_count'] >= 1
```

---

## 5. Hardware Requirements for Gen T

### 5.1 BR Configuration for PCIe Tunneling
```c
// BR Gen T Configuration
br_config_t gen_t_config = {
    .router_mode = USB4_MODE,
    .pcie_lanes = 4,              // Full x4 width
    .pcie_gen = PCIE_GEN4,        // 16GT/s per lane
    .tunnel_mode = PCIE_ONLY,     // or PCIE_PLUS_DP
    .hot_plug_enable = TRUE,
    .pm_enable = FALSE,           // Disable PM for stress testing
};
```

### 5.2 M.2 SSD Requirements
| Parameter | Requirement |
|-----------|-------------|
| Interface | PCIe Gen4 x4 |
| Protocol | NVMe 1.4+ |
| Capacity | ≥256GB |
| Endurance | High TBW (test grade) |
| Form Factor | M.2 2280 |
| Hot Plug | Supported |

### 5.3 Retimer Requirements
- DS100BR410 (TI) configured for PCIe Gen4
- Proper equalization for tunnel path
- Low jitter oscillator

---

## 6. Software API for Gen T

### 6.1 New API Methods
```python
class ThunderCat6:
    # Gen T PCIe Tunnel Methods
    
    def get_pcie_tunnel_status(self) -> dict:
        """Get PCIe tunnel status"""
        return {
            'link_up': bool,
            'width': int,         # 1, 2, or 4
            'speed': str,         # 'Gen3' or 'Gen4'
            'ltssm_state': str,
            'error_count': int,
            'recovery_count': int
        }
    
    def set_pcie_width(self, width: int):
        """Force PCIe width (1, 2, or 4)"""
        pass
    
    def inject_link_error(self, count: int):
        """Inject PCIe link errors for recovery testing"""
        pass
    
    def run_ssd_benchmark(self, test_size_gb: int, 
                          queue_depth: int = 32,
                          num_jobs: int = 4) -> dict:
        """Run SSD benchmark through PCIe tunnel"""
        pass
    
    def check_ssd_enumerated(self) -> bool:
        """Check if SSD is visible to host OS"""
        pass
    
    def safe_eject_ssd(self):
        """Safely eject SSD before disconnect"""
        pass
    
    def get_tunnel_bandwidth(self) -> dict:
        """Get real-time tunnel bandwidth usage"""
        pass
```

### 6.2 Register Interface
| Offset | Name | R/W | Description |
|--------|------|-----|-------------|
| 0x40 | PCIE_CTRL | RW | PCIe tunnel control |
| 0x41 | PCIE_STATUS | R | PCIe tunnel status |
| 0x42 | PCIE_WIDTH | RW | Negotiated/forced width |
| 0x43 | PCIE_SPEED | RW | Negotiated/forced speed |
| 0x44 | PCIE_ERR_CNT | R | Error counter |
| 0x45 | PCIE_RCV_CNT | R | Recovery counter |
| 0x48 | PCIE_BW_TX | R | TX bandwidth (100MB/s units) |
| 0x49 | PCIE_BW_RX | R | RX bandwidth (100MB/s units) |

---

## 7. Gen T Validation Checklist

- [ ] PCIe tunnel establishes within 5 seconds
- [ ] SSD enumerated correctly on host
- [ ] Read bandwidth ≥3GB/s (x4 Gen4)
- [ ] Write bandwidth ≥2.5GB/s (x4 Gen4)
- [ ] Hot plug works 100+ cycles
- [ ] Mixed tunnel (PCIe + DP) stable
- [ ] Link recovery within 100ms
- [ ] Power management transitions work
- [ ] Surprise removal handled gracefully
- [ ] Security/authentication correct

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| 0.1 | 2026-05-30 | AI | Initial Gen T specification |
