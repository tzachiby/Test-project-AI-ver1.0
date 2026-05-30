"""
ThunderCat6 Constants

TODO: Populate from datasheets
- I2C addresses from IC datasheets
- GPIO assignments from schematic
- Register definitions from IC datasheets
"""

# =============================================================================
# TODO: I2C Addresses - From datasheets
# =============================================================================
# I2C_ADDR_BR = 0x??      # TODO: From BR datasheet
# I2C_ADDR_KR = 0x??      # TODO: From KR datasheet
# I2C_ADDR_FX20 = 0x??    # TODO: From FX20 datasheet
# I2C_ADDR_PD = 0x??      # TODO: From PMG1-S3 datasheet
# I2C_ADDR_MST = 0x??     # TODO: From RTD2198 datasheet

# =============================================================================
# TODO: GPIO Assignments - From schematic
# =============================================================================
# GPIO_xxx = ?            # TODO: Define after schematic

# =============================================================================
# TODO: Mode Definitions - From requirements
# =============================================================================
# Modes from TC6 requirements (valid):
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
