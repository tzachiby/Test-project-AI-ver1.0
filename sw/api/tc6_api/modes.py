"""
ThunderCat6 Operating Modes
"""

from enum import Enum, auto


class TC6Mode(Enum):
    """
    ThunderCat6 operating modes.
    
    Each mode configures the card for specific testing scenarios.
    """
    
    # Thunderbolt/USB4 Tunnel Modes
    USB4 = auto()           # USB4 tunneled mode
    TBT3 = auto()           # Thunderbolt 3 tunneled mode
    PCIE_TUNNEL = auto()    # PCIe tunneled (via TBT/USB4)
    DP_TUNNEL = auto()      # DP tunneled (via TBT/USB4)
    USB_TUNNEL = auto()     # USB tunneled (via TBT/USB4)
    
    # Alt Modes
    DP_ALT = auto()         # DisplayPort Alt Mode
    MFD = auto()            # Multi-Function Device (USB + DP)
    
    # Native USB Modes
    USB_NATIVE_GEN1X1 = auto()  # USB 3.2 Gen1x1 (5Gbps)
    USB_NATIVE_GEN1X2 = auto()  # USB 3.2 Gen1x2 (10Gbps)
    USB_NATIVE_GEN2X1 = auto()  # USB 3.2 Gen2x1 (10Gbps)
    USB_NATIVE_GEN2X2 = auto()  # USB 3.2 Gen2x2 (20Gbps)
    
    # Special Modes
    EMPTY_DONGLE = auto()   # No device connected (pass-through)
    NDA = auto()            # No Device Attached (BR/KR disconnected)
    BYPASS = auto()         # Direct UFP to DFP bypass
    
    def __str__(self) -> str:
        return self.name
        
    @classmethod
    def from_string(cls, mode_str: str) -> "TC6Mode":
        """Convert string to TC6Mode enum."""
        try:
            return cls[mode_str.upper()]
        except KeyError:
            raise ValueError(f"Unknown mode: {mode_str}")


class TC6SubMode(Enum):
    """
    Sub-modes for specific configurations.
    """
    
    # DP configurations
    DP_MST = auto()         # Multi-Stream Transport
    DP_SST = auto()         # Single-Stream Transport
    DP_HBR3 = auto()        # HBR3 bitrate
    DP_UHBR10 = auto()      # UHBR10 bitrate
    DP_UHBR13_5 = auto()    # UHBR13.5 bitrate
    DP_UHBR20 = auto()      # UHBR20 bitrate
    
    # USB sub-modes
    USB_BULK = auto()       # Bulk transfer mode
    USB_ISOC = auto()       # Isochronous transfer mode
    USB_INTERRUPT = auto()  # Interrupt transfer mode
    
    # LPM states
    USB_U0 = auto()         # Active state
    USB_U1 = auto()         # Standby (fast exit)
    USB_U2 = auto()         # Standby (slow exit)
    USB_U3 = auto()         # Suspend
    
    def __str__(self) -> str:
        return self.name
