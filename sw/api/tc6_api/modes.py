"""
ThunderCat6 Mode Definitions

Modes are defined based on TC6 requirements document.
"""

from enum import Enum


class TC6Mode(Enum):
    """
    TC6 operation modes from requirements.
    
    These mode names are from the TC6 requirements document.
    Implementation details TBD after obtaining datasheets.
    """
    
    # Tunnel Modes
    TBT4_TUNNEL = "tbt4_tunnel"        # TBT4 with PCIe + DP + USB
    USB4_TUNNEL = "usb4_tunnel"        # USB4 native mode
    
    # USB3 Native Modes (NEW in TC6)
    USB3_GEN2X2 = "usb3_gen2x2"        # 20 Gbps (2 lanes x 10 Gbps)
    USB3_GEN2X1 = "usb3_gen2x1"        # 10 Gbps (1 lane x 10 Gbps)
    USB3_GEN1X2 = "usb3_gen1x2"        # 10 Gbps (2 lanes x 5 Gbps)
    USB3_GEN1X1 = "usb3_gen1x1"        # 5 Gbps (1 lane x 5 Gbps)
    
    # Alt Modes
    DP_ALT_MODE = "dp_alt_mode"        # DP 2.0/2.1 Alt Mode
    
    # Multi-Function
    MFD = "mfd"                        # USB3 + DP combined
    
    # Special Modes (NEW in TC6)
    EMPTY_DONGLE = "empty_dongle"      # No connection
    NDA = "nda"                        # BR/KR disconnected


# TODO: Mode switching implementation after control interface defined
# TODO: Mode configuration registers from IC datasheets
