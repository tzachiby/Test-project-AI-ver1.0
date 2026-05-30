"""
ThunderCat6 Host API
====================

TODO: API is placeholder - implement after obtaining IC datasheets

Current status:
- Mode definitions from TC6 requirements (valid)
- All controller implementations are TODO

Required before implementation:
- BR (Barlow Ridge) datasheet
- KR (Kite Ridge) datasheet
- FX20 datasheet
- PMG1-S3 datasheet
- Control interface definition (FTDI, MCU, etc.)
"""

from .modes import TC6Mode

__version__ = "0.1.0"
__author__ = "ThunderCat Team"
__status__ = "PLACEHOLDER - Awaiting datasheets"

__all__ = [
    "TC6Mode",
]

# TODO: Add imports after implementing controllers
# from .thundercat6 import ThunderCat6
# from .mux_control import HighSpeedMux
# from .fx20_controller import FX20Controller
# from .gen_t_controller import GenTController
