"""
ThunderCat6 Host API
====================

Python API for controlling ThunderCat6 test cards.

Usage:
    from tc6_api import ThunderCat6

    tc6 = ThunderCat6(port="COM3")
    tc6.connect()
    tc6.set_mode("USB4")
    tc6.disconnect()
"""

from .thundercat6 import ThunderCat6
from .modes import TC6Mode
from .constants import *

__version__ = "0.1.0"
__author__ = "ThunderCat Team"
__all__ = ["ThunderCat6", "TC6Mode"]
