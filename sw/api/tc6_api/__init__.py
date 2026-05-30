"""
ThunderCat6 Host API
====================

Python API for controlling ThunderCat6 test cards.

Usage:
    from tc6_api import ThunderCat6, MuxPath, USBSpeed

    tc6 = ThunderCat6(port="COM3")
    tc6.connect()
    
    # Set mode to USB native with speed downgrade
    tc6.set_mode("USB_NATIVE")
    tc6.mux.enable_br_bypass()  # Direct FX20 path
    tc6.speed.set_speed(USBSpeed.GEN1_X1)  # 5 Gbps, 1 lane
    
    tc6.disconnect()
"""

from .thundercat6 import ThunderCat6
from .modes import TC6Mode
from .constants import *
from .mux_control import HighSpeedMux, MuxPath, USBSpeed, USBSpeedController
from .fx20_controller import FX20Controller, LPMState, USBProtocol
from .gen_t_controller import (
    GenTController, GenTMode, PCIeSpeed, PCIeWidth, 
    PCIeTunnelStatus, BandwidthStats, BenchmarkResult
)

__version__ = "0.1.0"
__author__ = "ThunderCat Team"

__all__ = [
    "ThunderCat6",
    "TC6Mode",
    "HighSpeedMux",
    "MuxPath",
    "USBSpeed",
    "USBSpeedController",
    "FX20Controller",
    "LPMState",
    "USBProtocol",
    # Gen T (PCIe Tunneling)
    "GenTController",
    "GenTMode",
    "PCIeSpeed",
    "PCIeWidth",
    "PCIeTunnelStatus",
    "BandwidthStats",
    "BenchmarkResult",
]
