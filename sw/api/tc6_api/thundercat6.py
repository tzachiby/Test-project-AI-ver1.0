"""
ThunderCat6 Main API Class
"""

import serial
import time
from typing import Optional, Dict, Any
from .modes import TC6Mode
from .constants import *


class ThunderCat6:
    """
    Main class for controlling ThunderCat6 test cards.
    
    Provides high-level API for:
    - Mode switching (USB4, TBT3, DP, MFD, USB Native)
    - Device reset and control
    - Status monitoring
    - Firmware management
    
    Example:
        tc6 = ThunderCat6(port="COM3")
        tc6.connect()
        tc6.set_mode(TC6Mode.USB4)
        print(tc6.get_status())
        tc6.disconnect()
    """
    
    def __init__(self, port: str = "COM3", baudrate: int = 115200):
        """
        Initialize ThunderCat6 connection.
        
        Args:
            port: Serial port for FTDI backdoor connection
            baudrate: Serial baudrate (default: 115200)
        """
        self.port = port
        self.baudrate = baudrate
        self._serial: Optional[serial.Serial] = None
        self._connected = False
        self._current_mode: Optional[TC6Mode] = None
        
    def connect(self) -> bool:
        """
        Establish connection to ThunderCat6 card.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self._serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1
            )
            self._connected = True
            self._read_current_mode()
            return True
        except serial.SerialException as e:
            print(f"Connection failed: {e}")
            return False
            
    def disconnect(self) -> None:
        """Close connection to ThunderCat6 card."""
        if self._serial and self._serial.is_open:
            self._serial.close()
        self._connected = False
        
    def is_connected(self) -> bool:
        """Check if connected to ThunderCat6."""
        return self._connected and self._serial and self._serial.is_open
        
    def get_card_info(self) -> Dict[str, Any]:
        """
        Get ThunderCat6 card information.
        
        Returns:
            Dictionary with card info (serial, FW version, DIP switch, etc.)
        """
        self._check_connection()
        # TODO: Implement actual card info reading
        return {
            "model": "ThunderCat6",
            "serial": "TC6-XXXX-XXXX",
            "fw_version": "0.1.0",
            "dip_switch": self._read_dip_switch(),
            "current_mode": str(self._current_mode)
        }
        
    def set_mode(self, mode: TC6Mode, timeout: float = 7.0) -> bool:
        """
        Switch to specified operating mode.
        
        Args:
            mode: Target mode (TC6Mode enum)
            timeout: Maximum time to wait for mode switch (default: 7s)
            
        Returns:
            True if mode switch successful, False otherwise
        """
        self._check_connection()
        
        if self._current_mode == mode:
            return True
            
        # TODO: Implement actual mode switching via FTDI/PD
        print(f"Switching from {self._current_mode} to {mode}...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            # Simulate mode switch
            time.sleep(0.5)
            self._current_mode = mode
            return True
            
        return False
        
    def get_mode(self) -> TC6Mode:
        """Get current operating mode."""
        self._check_connection()
        return self._current_mode
        
    def reset(self, component: str = "all") -> bool:
        """
        Reset ThunderCat6 or specific component.
        
        Args:
            component: "all", "br", "kr", "fx20", "pd", "mst"
            
        Returns:
            True if reset successful
        """
        self._check_connection()
        # TODO: Implement actual reset logic
        print(f"Resetting {component}...")
        time.sleep(0.5)
        return True
        
    def get_status(self) -> Dict[str, Any]:
        """
        Get current status of all components.
        
        Returns:
            Dictionary with component statuses
        """
        self._check_connection()
        # TODO: Implement actual status reading
        return {
            "br_link": True,
            "kr_link": False,
            "usb_connected": True,
            "dp_connected": False,
            "pcie_connected": True,
            "error_flags": 0x00
        }
        
    def read_endpoint_info(self) -> Dict[str, Any]:
        """
        Read endpoint device information (SSD, etc.).
        
        Returns:
            Dictionary with endpoint info
        """
        self._check_connection()
        # TODO: Implement via UFP
        return {
            "ssd_model": "Unknown",
            "ssd_fw_version": "Unknown",
            "ssd_capacity_gb": 0
        }
        
    def set_usb_speed(self, gen: int, width: int) -> bool:
        """
        Set USB speed/width (Gen1x1, Gen1x2, Gen2x1, Gen2x2).
        
        Args:
            gen: USB generation (1 or 2)
            width: Lane width (1 or 2)
            
        Returns:
            True if successful
        """
        self._check_connection()
        # TODO: Implement via PD control / High-Speed Mux
        print(f"Setting USB Gen{gen}x{width}...")
        return True
        
    def assert_hpd(self, state: bool) -> bool:
        """
        Assert/deassert HPD (Hot Plug Detect) signal.
        
        Args:
            state: True to assert, False to deassert
            
        Returns:
            True if successful
        """
        self._check_connection()
        # TODO: Implement HPD control
        return True
        
    def read_fw_version(self, component: str) -> str:
        """
        Read firmware version of a component.
        
        Args:
            component: "br", "kr", "pd", "ftdi", "fx20", "mst"
            
        Returns:
            Firmware version string
        """
        self._check_connection()
        # TODO: Implement actual FW reading
        return "0.0.0"
        
    def _check_connection(self) -> None:
        """Verify connection is active."""
        if not self.is_connected():
            raise RuntimeError("Not connected to ThunderCat6")
            
    def _read_current_mode(self) -> None:
        """Read current mode from card."""
        # TODO: Implement actual mode reading
        self._current_mode = TC6Mode.USB4
        
    def _read_dip_switch(self) -> int:
        """Read DIP switch value."""
        # TODO: Implement actual DIP reading via FTDI
        return 0
        
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
        return False
