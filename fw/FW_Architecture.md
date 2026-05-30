# ThunderCat6 Firmware Architecture

## 1. Overview

ThunderCat6 firmware components run on multiple embedded processors across the board.
This document defines the FW architecture for each major IC.

---

## 2. Firmware Components Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ThunderCat6 Firmware Stack                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │  BR FW      │    │  KR FW      │    │  FX20 FW    │    │  PD FW      │ │
│  │  (Intel)    │    │  (Intel)    │    │  (Cypress)  │    │  (Infineon) │ │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘ │
│         │                  │                  │                  │         │
│         └──────────────────┼──────────────────┼──────────────────┘         │
│                            │                  │                             │
│                            ▼                  ▼                             │
│                    ┌─────────────────────────────────────┐                 │
│                    │       FTDI Configuration            │                 │
│                    │       (EEPROM + Host Control)       │                 │
│                    └─────────────────────────────────────┘                 │
│                                      │                                      │
│                                      ▼                                      │
│                    ┌─────────────────────────────────────┐                 │
│                    │        Host PC (Python API)         │                 │
│                    │        tc6_api Package              │                 │
│                    └─────────────────────────────────────┘                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Barlow Ridge (BR) Firmware

### 3.1 Overview
| Property | Value |
|----------|-------|
| **Vendor** | Intel |
| **Type** | Binary Blob + Configuration |
| **Flash** | External SPI (16Mbit) |
| **Update Method** | SPI via FTDI / TBT NVM |

### 3.2 Configuration Parameters
```c
// BR Configuration Structure
typedef struct {
    uint8_t  router_mode;        // 0=USB4, 1=TBT3, 2=TBT4
    uint8_t  dp_output_count;    // 1-4 DP outputs
    uint8_t  pcie_lanes;         // 2 or 4 lanes
    uint8_t  usb3_enabled;       // 0=disabled, 1=enabled
    uint16_t vendor_id;          // 0x8086 (Intel)
    uint16_t device_id;          // TC6 specific
    char     product_name[32];   // "ThunderCat6"
    uint8_t  security_level;     // 0=None, 1=User, 2=Secure
} br_config_t;
```

### 3.3 Modes of Operation
| Mode | BR Config | Description |
|------|-----------|-------------|
| TBT4 Tunnel | router_mode=2 | Full Thunderbolt 4 device |
| USB4 Tunnel | router_mode=0 | USB4 compliant operation |
| USB3 Bypass | usb3_enabled=0 | Forces USB3 to external path |

### 3.4 Programming Interface
- **SPI Flash Programming**: Via FTDI Channel C
- **Runtime Config**: I2C (0x37) for limited parameters
- **Debug Console**: UART on FTDI Channel A

---

## 4. Kite Ridge (KR) Firmware

### 4.1 Overview
| Property | Value |
|----------|-------|
| **Vendor** | Intel |
| **Type** | USB4 Retimer Configuration |
| **Flash** | Internal OTP + I2C Shadow |
| **Update Method** | I2C registers |

### 4.2 Configuration Parameters
```c
// KR Configuration Structure
typedef struct {
    uint8_t  link_rate;          // 0=Gen2, 1=Gen3
    uint8_t  lane_count;         // 1, 2, or 4
    uint8_t  eq_preset;          // Equalization preset 0-15
    uint8_t  retimer_mode;       // 0=Passive, 1=Active
    uint8_t  usb4_mode;          // 0=USB4, 1=USB3.2
    uint16_t rx_ctle;            // RX CTLE settings
    uint16_t tx_pre_emphasis;    // TX Pre-emphasis
} kr_config_t;
```

### 4.3 Equalization Profiles
| Profile | Use Case | Settings |
|---------|----------|----------|
| Default | Short traces (<4") | EQ preset 3 |
| Extended | Long traces (4-8") | EQ preset 7 |
| Cable | External cables | EQ preset 12 |

---

## 5. FX20 Firmware

### 5.1 Overview
| Property | Value |
|----------|-------|
| **Vendor** | Cypress/Infineon |
| **Type** | Full FW Image |
| **Flash** | Internal Flash |
| **Update Method** | I2C Bootloader / USB DFU |

### 5.2 FW Modules
```
┌─────────────────────────────────────────┐
│             FX20 Firmware               │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────┐   │
│  │      USB Protocol Stack          │   │
│  │  • USB 3.2 Gen1/Gen2/Gen2x2     │   │
│  │  • USB 2.0 HS/FS                │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │      Traffic Generator          │   │
│  │  • Bulk Loopback                │   │
│  │  • Interrupt Patterns           │   │
│  │  • Isochronous Streams          │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │      LPM Controller             │   │
│  │  • U1/U2/U3 Entry/Exit          │   │
│  │  • L1.1/L1.2 Support            │   │
│  │  • Deep Sleep Mode              │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │      I2C Slave Interface        │   │
│  │  • Command Registers            │   │
│  │  • Status Registers             │   │
│  │  • Configuration                │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### 5.3 Register Map
| Offset | Name | R/W | Description |
|--------|------|-----|-------------|
| 0x00 | DEV_ID | R | Device ID (0x20) |
| 0x01 | VERSION | R | FW Version |
| 0x02 | STATUS | R | Status Flags |
| 0x03 | CONTROL | RW | Control Register |
| 0x04 | USB_SPEED | RW | Speed: 0=HS, 1=SS1, 2=SS2, 3=SS2x2 |
| 0x05 | LPM_STATE | RW | LPM State Control |
| 0x06 | TRAFFIC_MODE | RW | Traffic Pattern |
| 0x07 | LOOPBACK_EN | RW | Loopback Enable |
| 0x08-0x0F | EP_CONFIG | RW | Endpoint Configuration |
| 0x10-0x1F | COUNTERS | R | Traffic Counters |

### 5.4 Traffic Modes
```c
typedef enum {
    FX20_MODE_IDLE       = 0x00,
    FX20_MODE_LOOPBACK   = 0x01,
    FX20_MODE_SOURCE     = 0x02,
    FX20_MODE_SINK       = 0x03,
    FX20_MODE_PATTERN    = 0x04,
    FX20_MODE_STRESS     = 0x05
} fx20_traffic_mode_t;
```

---

## 6. PMG1-S3 (PD Controller) Firmware

### 6.1 Overview
| Property | Value |
|----------|-------|
| **Vendor** | Infineon |
| **Type** | Configuration Table + FW |
| **Flash** | Internal Flash |
| **Update Method** | I2C / EZ-PD Config Utility |

### 6.2 PD Configuration
```c
// PD Configuration
typedef struct {
    // Source Capabilities
    uint32_t src_pdo[7];         // Up to 7 PDOs
    uint8_t  src_pdo_count;
    
    // Sink Capabilities  
    uint32_t snk_pdo[7];
    uint8_t  snk_pdo_count;
    
    // DRP Configuration
    uint8_t  port_role;          // 0=Sink, 1=Source, 2=DRP
    uint8_t  try_src;            // Try.SRC enable
    uint8_t  try_snk;            // Try.SNK enable
    
    // Features
    uint8_t  pd_revision;        // 2=PD2.0, 3=PD3.0
    uint8_t  fast_role_swap;     // FRS enable
    uint8_t  usb4_support;       // USB4 enter mode
} pd_config_t;
```

### 6.3 Power Profiles for TC6
| Profile | PDO Config | Max Power |
|---------|------------|-----------|
| Default Sink | 5V@3A, 9V@3A, 12V@3A | 36W |
| Test Source | 5V@3A, 9V@3A, 12V@3A, 20V@5A | 100W |
| USB-C Only | 5V@3A | 15W |

---

## 7. FTDI Configuration

### 7.1 EEPROM Layout
```
┌─────────────────────────────────────────┐
│          FT4232H EEPROM (2Kbit)         │
├─────────────────────────────────────────┤
│ 0x00-0x07: Header & Config              │
│ 0x08-0x09: VID (0x0403)                 │
│ 0x0A-0x0B: PID (Custom)                 │
│ 0x0C-0x0D: Device Version               │
│ 0x0E-0x0F: Config Flags                 │
│ 0x10-0x11: Max Power (mA)               │
│ 0x12-0x3F: Reserved                     │
│ 0x40-0x5F: Manufacturer String          │
│ 0x60-0x7F: Product String               │
│ 0x80-0x9F: Serial Number                │
│ 0xA0-0xBF: Channel A Config             │
│ 0xC0-0xDF: Channel B Config             │
│ 0xE0-0xFF: GPIO Default States          │
└─────────────────────────────────────────┘
```

### 7.2 Channel Configuration
| Channel | Mode | Speed | Use |
|---------|------|-------|-----|
| A | UART | 115200-921600 | Debug Console |
| B | I2C | 400kHz | Device Control |
| C | SPI | 20MHz | Flash Programming |
| D | GPIO | N/A | Control Signals |

### 7.3 GPIO Pin Mapping
| GPIO | Direction | Function |
|------|-----------|----------|
| ACBUS0 | Output | MUX_SEL0 |
| ACBUS1 | Output | MUX_SEL1 |
| ACBUS2 | Output | MUX_SEL2 |
| ACBUS3 | Output | BR_RESET_N |
| ACBUS4 | Output | KR_RESET_N |
| ACBUS5 | Output | FX20_RESET_N |
| ACBUS6 | Output | MST_RESET_N |
| ACBUS7 | Output | LED_CTRL |
| ADBUS0 | Input | DIP_SW0 |
| ADBUS1 | Input | DIP_SW1 |
| ADBUS2 | Input | DIP_SW2 |
| ADBUS3 | Input | DIP_SW3 |

---

## 8. Firmware Update Procedures

### 8.1 BR NVM Update
```python
def update_br_nvm(image_path: str):
    """Update BR NVM via TBT connection or SPI"""
    # Method 1: Via Thunderbolt (preferred)
    tbt_nvm_update(image_path)
    
    # Method 2: Via SPI (fallback)
    spi = ftdi.open_spi(channel='C')
    spi.chip_erase()
    spi.program(image_path)
    spi.verify(image_path)
```

### 8.2 FX20 Update
```python
def update_fx20_fw(image_path: str):
    """Update FX20 via I2C bootloader"""
    i2c = ftdi.open_i2c(channel='B')
    
    # Enter bootloader
    i2c.write(FX20_ADDR, [0xFF, 0x01])  # Reset to BL
    time.sleep(0.1)
    
    # Program
    with open(image_path, 'rb') as f:
        data = f.read()
    
    for offset in range(0, len(data), 64):
        chunk = data[offset:offset+64]
        i2c.write(FX20_BL_ADDR, [offset >> 8, offset & 0xFF] + list(chunk))
    
    # Exit bootloader
    i2c.write(FX20_BL_ADDR, [0x00, 0x00])  # Jump to app
```

### 8.3 PD Config Update
```python
def update_pd_config(config: pd_config_t):
    """Update PD controller configuration"""
    i2c = ftdi.open_i2c(channel='B')
    
    # Write configuration table
    i2c.write(PMG1_ADDR, [0x80] + config.to_bytes())
    
    # Trigger config reload
    i2c.write(PMG1_ADDR, [0x00, 0x01])  # RESET command
```

---

## 9. Debug & Logging

### 9.1 UART Debug Console
```
Connected to ThunderCat6 Debug Console v1.0
> help
Commands:
  status      - Show system status
  reset       - Reset all components
  mode <n>    - Set operation mode
  pd <cmd>    - PD controller commands
  fx20 <cmd>  - FX20 commands
  br <cmd>    - BR commands
  i2c <cmd>   - I2C operations
  gpio <cmd>  - GPIO control
  log <lvl>   - Set log level

> status
BR:   Connected, TBT4 mode
KR:   Active, Gen3 x4
FX20: Idle, USB3 Gen2
PD:   Sink @ 12V/3A
DIP:  0x3 (USB4 Tunnel)
```

### 9.2 Log Levels
| Level | Description |
|-------|-------------|
| 0 | OFF |
| 1 | ERROR |
| 2 | WARN |
| 3 | INFO |
| 4 | DEBUG |
| 5 | TRACE |

---

## 10. Build Instructions

### 10.1 FX20 FW Build
```bash
# Requires Cypress/Infineon SDK
cd fw/fx20
make clean
make CONFIG=tc6_release
# Output: build/fx20_tc6.img
```

### 10.2 PD Config Build
```bash
# Requires EZ-PD Configuration Utility
cd fw/pd
python gen_pd_config.py --input tc6_pd.json --output tc6_pd.cyacd
```

### 10.3 FTDI EEPROM Build
```bash
# Requires FT_Prog or libftdi
cd fw/ftdi
ftdi_eeprom --flash-eeprom tc6_ftdi.conf
```

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| 0.1 | 2026-05-30 | AI | Initial FW architecture |
