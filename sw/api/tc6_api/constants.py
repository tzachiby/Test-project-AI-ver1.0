"""
ThunderCat6 Constants

Specifications from datasheets:
- Kite Ridge 0.76 (March 2026)
- Barlow Ridge Accessory Training v1.2
- Tornado Ridge 0.5 Draft
"""

# =============================================================================
# KR (Kite Ridge) Specifications - From Kite Ridge 0.76 Datasheet
# =============================================================================
# I2C Interface
KR_I2C_PINS = {
    'SCL': 'I2C_SCL',
    'SDA': 'I2C_SDA',
    'INT': 'I2C_INT',
}
# I2C can be configured as Master or Slave
# Transaction: Start → Slave addr (7b + R/W) → Reg offset [7:0] → Size [7:0] → Data

# SPI Interface
KR_SPI_MIN_CLOCK_MHZ = 50
KR_SPI_VOLTAGE = 1.8  # V
KR_SPI_SECTOR_SIZE = 4096  # 4KB
KR_SPI_COMMANDS = {
    'WREN': 0x06,
    'WRDI': 0x04,
    'RDSR': 0x05,
    'FAST_READ': 0x0B,
    'PP': 0x02,
    'SE': 0x20,
    'DUAL_OUT': 0x3B,
}

# KR Power Rails (From Datasheet)
KR_POWER_RAILS = {
    'VCC1P8_SX': {'min': 1.71, 'typ': 1.8, 'max': 1.89, 'max_current_ma': 200},
    'VCC1P8_SX_IO': {'typ': 1.8, 'max_current_ma': 100},
    'VCC1P2': {'min': 1.14, 'typ': 1.2, 'max': 1.26, 'max_current_ma': 1250},
    'VCC0P8': {'min': 0.7, 'typ': 0.8, 'max': 0.9, 'max_current_a': 4},  # Adjustable via SVR_CNTL
}

# KR Reset Timing
KR_RESET_DELAY_US = 100  # RESET_N deasserted min 100μs after VCC1P8_SX reaches 90%
KR_RESET_RISE_TIME_NS = (0.1, 500)  # min, max ns

# KR Supported Speeds (From Datasheet)
KR_USB4_SPEEDS = {
    'GEN4': '40Gbps (PAM3)',
    'GEN3': '20.625/20.0Gbps',
    'GEN2': '10.3125/10.0Gbps',
}
KR_USB32_SPEEDS = {
    'GEN2X2': '20Gbps',
    'GEN2X1': '10Gbps',
}
KR_DP_SPEEDS = ['UHBR20G', 'UHBR10G', 'HBR3', 'UHBR13.5']
KR_PCIE_SUPPORT = 'Gen5 tunneling'
KR_TBT_SUPPORT = 'Gen3 compatible'

# KR Crystal Requirements
KR_XTAL_FREQ_MHZ = 25.0
KR_XTAL_TOLERANCE_PPM = 30
KR_XTAL_LOAD_PF = 20
KR_XTAL_ESR_MAX_OHM = 50

# KR Digital I/O (1.8V)
KR_IO_VOH_MIN = 1.4  # V
KR_IO_VOL_MAX = 0.4  # V
KR_IO_PU_KOHM = (31, 79)  # min, max internal pull-up
KR_IO_PD_KOHM = (31, 68)  # min, max internal pull-down

# KR Thermal
KR_TEMP_AMBIENT_C = (0, 55)  # Operating range
KR_TEMP_JUNCTION_MAX_C = 110
# Thermal diode equation: Tj [°C] = 600.52 – 712.02 × V[v] (at 1mA)
KR_THERMAL_DIODE_COEFFS = {'offset': 600.52, 'slope': -712.02, 'current_ma': 1}

# KR SBU MUX Timing
KR_SBU_MUX_DELAY_MS = 20  # Min delay after mode entry ACK

# =============================================================================
# BR (Barlow Ridge) Specifications - From Accessory Training v1.2
# =============================================================================
# LC GPIOs (1.8V_Sx Domain)
BR_LC_GPIO = {
    'GPIO_0': {'ball': 'AC17', 'name': 'PM_PCIE_S0_EN', 'type': 'OUT', 'config': '100kΩ PD'},
    'GPIO_1': {'ball': 'AC18', 'name': 'PM_MST_RST_N', 'type': 'OUT', 'config': '10kΩ PU to 1.8V'},
    'GPIO_3': {'ball': 'AC16', 'name': 'I2C_SCL', 'type': 'OD', 'config': '1kΩ PU to 1.8V'},
    'GPIO_4': {'ball': 'AC8', 'name': 'I2C_SDA', 'type': 'OD', 'config': '1kΩ PU to 1.8V'},
    'GPIO_7': {'ball': 'AC10', 'name': 'TMU_CLKIN', 'type': 'IN'},
    'GPIO_8': {'ball': 'AC23', 'name': 'TMU_CLKOUT', 'type': 'OUT'},
}

# POC GPIOs (Power-On Control)
BR_POC_GPIO = {
    'POC_GPIO_0': {'ball': 'L21', 'name': 'PA_BIDIR_IN_EN', 'type': 'OUT', 'config': '100kΩ PD'},
    'POC_GPIO_1': {'ball': 'V21', 'name': 'PB_BIDIR_IN_EN', 'type': 'OUT', 'config': '100kΩ PD'},
    'POC_GPIO_2': {'ball': 'AC22', 'name': 'PAB_I2CINT_N', 'type': 'IN', 'config': '10kΩ PU'},
    'POC_GPIO_4': {'ball': 'K21', 'name': 'PCIE_WAKE_N', 'type': 'IN', 'config': '10kΩ PU'},
    'POC_GPIO_5': {'ball': 'F13', 'name': 'PM_PCIE_EN', 'type': 'OUT', 'config': '100kΩ PD'},
    'POC_GPIO_6': {'ball': 'M23', 'name': 'FORCE_WAKE', 'type': 'IN', 'config': '10kΩ PD'},
    'POC_GPIO_7': {'ball': 'N21', 'name': 'PCIE_RESET_N', 'type': 'OUT', 'config': '10kΩ PD'},
    'POC_GPIO_8': {'ball': 'F11', 'name': 'SMBUS_SCL', 'type': 'OD', 'config': '330Ω PU'},
    'POC_GPIO_9': {'ball': 'F12', 'name': 'SMBUS_SDA', 'type': 'OD', 'config': '330Ω PU'},
}

# BR SVR (Switching Voltage Regulator) Specs
BR_SVR_0P75 = {
    'vout_range': (0.67, 0.924),  # V
    'vout_step_mv': 1.0,
    'steps': 256,
    'max_current_a': 3,
    'switching_freq_mhz': 1,
    'ripple_mv': 10,
    'inductor_uh': 0.4,
    'inductor_tolerance': 0.2,
    'inductor_esr_mohm': 8.3,
    'cin_options': ['2×22µF', '4×10µF'],
    'cout_options': ['6×22µF', '12×10µF'],
}

BR_SVR_1P2 = {
    'vout_range': (1.07, 1.47),  # V
    'vout_step_mv': 1.6,
    'steps': 256,
    'max_current_a': 1,
    'switching_freq_mhz': 1,
    'ripple_mv': 10,
    'inductor_uh': 0.6,
    'inductor_tolerance': 0.2,
    'inductor_esr_mohm': 43,
    'cin_options': ['1×22µF', '2×10µF'],
    'cout_options': ['4×22µF', '8×10µF'],
}

# =============================================================================
# TR (Tornado Ridge) Specifications - From Draft Document
# =============================================================================
TR_VERSION = '0.5 Draft (July 2025)'
TR_BASE = 'Kite Ridge'

TR_OPERATIONAL_MODES = {
    'PCIE_MINI_DOCK': {
        'description': 'TBT3/USB4 with PCIe tunneling',
        'pcie_lanes': 4,
        'pcie_speed_gbps_per_lane': 32,
        'bifurcation': ['1x4', '4x1', '2x2', '1x2+2x1'],
    },
    'STORAGE': {
        'description': 'USB4/TBT3/USB3/MFDP upstream, single NVMe endpoint',
    },
}

TR_PROTOCOL_SUPPORT = ['PCIe Gen5', 'USB4 v2.0 (symmetric)', 'TBT Gen3', 'USB3.2 Gen2x2', 'USB3.2 Gen2x1']

TR_POWER_RAILS = {
    'VCC1P8_SX': 1.8,
    'VCC1P2': 1.2,
    'VCC0P8': 0.8,  # Adjustable
    'VCC0P9': 0.9,
}

# SMBUS FW Update
TR_SMBUS_MAX_TRANSACTION = 128  # bytes
TR_SMBUS_NAK_RETRY_DELAY_MS = 10

# =============================================================================
# Board Design Requirements (From Datasheets)
# =============================================================================
PULLUP_CONFIG = {
    'I2C_LC': '1kΩ to 1.8V_Sx',
    'SMBUS': '330Ω to 1.8V_Sx',
    'RESET_N': '10kΩ to GND (pull-down)',
    'VBUS_EN': '100kΩ to GND (pull-down)',
    'HPD': '100kΩ to GND (pull-down)',
    'LSRX': '1MΩ to GND (pull-down)',
    'LSTX': '20kΩ to 1.8V_Sx (pull-up)',
}

# =============================================================================
# Mode Definitions (From TC6 Requirements - Valid)
# =============================================================================
MODES = [
    "TBT4_TUNNEL",      # TBT4 with PCIe + DP + USB
    "USB4_TUNNEL",      # USB4 native
    "USB3_GEN2X2",      # 20 Gbps
    "USB3_GEN2X1",      # 10 Gbps
    "USB3_GEN1X2",      # 10 Gbps
    "USB3_GEN1X1",      # 5 Gbps
    "DP_ALT_MODE",      # DP 2.0/2.1
    "MFD",              # Multi-Function Device
]
