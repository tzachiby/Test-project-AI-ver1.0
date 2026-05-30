"""
ThunderCat6 High-Speed Mux Control Module

Controls the high-speed mux routing between UFP and internal components.
Addresses TC5 Showstopper #1, #2, and High Priority #6.
"""

from enum import IntEnum
from typing import Optional


class MuxPath(IntEnum):
    """High-Speed Mux path selection."""
    BR_TUNNEL = 0b000      # UFP → BR (TBT/USB4 Tunnel)
    KR_NATIVE = 0b001      # UFP → KR (USB4 Native)
    FX20_DIRECT = 0b010    # UFP → FX20 (USB Native Direct) - BYPASSES BR
    DFP1_PASSTHROUGH = 0b011  # UFP → DFP1 (Pass-through)
    DFP2_PASSTHROUGH = 0b100  # UFP → DFP2 (Pass-through)


class USBSpeed(IntEnum):
    """USB speed/lane configuration for native USB mode."""
    GEN1_X1 = 0  # 5 Gbps, 1 lane
    GEN1_X2 = 1  # 5 Gbps, 2 lanes (10 Gbps aggregate)
    GEN2_X1 = 2  # 10 Gbps, 1 lane
    GEN2_X2 = 3  # 20 Gbps, 2 lanes


class HighSpeedMux:
    """
    High-Speed Mux Controller for ThunderCat6.
    
    Manages signal routing between UFP and internal components.
    Key feature: Enables USB native mode testing by bypassing BR.
    
    TC5 Limitations Addressed:
    - Cannot control BR USB Hub rate/width in Native USB mode
    - No bypass for commercial device testing
    - MFD USB/DP rate control not possible via BR
    
    TC6 Solution:
    - Direct FX20 connection bypassing BR
    - DFP pass-through for commercial devices
    - PD-controlled rate negotiation
    """
    
    # GPIO pins for mux control (on FTDI)
    GPIO_SEL0 = 0
    GPIO_SEL1 = 1
    GPIO_SEL2 = 2
    
    def __init__(self, ftdi_controller):
        """
        Initialize High-Speed Mux controller.
        
        Args:
            ftdi_controller: FTDI controller instance for GPIO access
        """
        self._ftdi = ftdi_controller
        self._current_path: Optional[MuxPath] = None
        
    def set_path(self, path: MuxPath) -> bool:
        """
        Set the high-speed mux path.
        
        Args:
            path: Target path from MuxPath enum
            
        Returns:
            True if path set successfully
            
        Example:
            # Bypass BR for native USB testing
            mux.set_path(MuxPath.FX20_DIRECT)
        """
        try:
            # Set GPIO bits for path selection
            sel_value = int(path)
            self._ftdi.set_gpio(self.GPIO_SEL0, (sel_value >> 0) & 1)
            self._ftdi.set_gpio(self.GPIO_SEL1, (sel_value >> 1) & 1)
            self._ftdi.set_gpio(self.GPIO_SEL2, (sel_value >> 2) & 1)
            
            self._current_path = path
            return True
        except Exception as e:
            print(f"Failed to set mux path: {e}")
            return False
            
    def get_path(self) -> Optional[MuxPath]:
        """Get current mux path setting."""
        return self._current_path
        
    def enable_br_bypass(self) -> bool:
        """
        Enable BR bypass for direct UFP-FX20 connection.
        
        Use this for:
        - Native USB speed testing (Gen1x1, Gen1x2, Gen2x1, Gen2x2)
        - USB protocol testing without TBT controller interference
        - LPM testing with FX20's full U1/U2/U3 support
        
        Returns:
            True if bypass enabled successfully
        """
        return self.set_path(MuxPath.FX20_DIRECT)
        
    def enable_dfp_passthrough(self, dfp_port: int = 1) -> bool:
        """
        Enable direct UFP-DFP pass-through for commercial device testing.
        
        Addresses High Priority #6: Complete bypass without BR/muxes.
        
        Args:
            dfp_port: DFP port number (1 or 2)
            
        Returns:
            True if pass-through enabled successfully
        """
        if dfp_port == 1:
            return self.set_path(MuxPath.DFP1_PASSTHROUGH)
        elif dfp_port == 2:
            return self.set_path(MuxPath.DFP2_PASSTHROUGH)
        else:
            raise ValueError(f"Invalid DFP port: {dfp_port}")
            
    def enable_tunnel_mode(self) -> bool:
        """
        Route signals through BR for tunnel mode.
        
        Default path for TBT3/TBT4/USB4 tunnel operations.
        
        Returns:
            True if tunnel mode enabled
        """
        return self.set_path(MuxPath.BR_TUNNEL)
        
    def enable_usb4_native(self) -> bool:
        """
        Route signals through KR for USB4 native mode.
        
        Addresses Showstopper #5: USB4v1 Gen3/Gen2 downgrade.
        
        Returns:
            True if USB4 native mode enabled
        """
        return self.set_path(MuxPath.KR_NATIVE)


class USBSpeedController:
    """
    USB Speed/Lane Controller for native USB mode.
    
    Addresses TC5 Showstopper #1:
    - Native USB speed downgrade not supported via BR
    - Need Gen1x1, Gen1x2, Gen2x1, Gen2x2 control
    
    TC6 Solution:
    - FX20 direct connection via high-speed mux
    - Speed control via FX20 registers
    """
    
    def __init__(self, fx20_controller, hs_mux: HighSpeedMux):
        """
        Initialize USB Speed Controller.
        
        Args:
            fx20_controller: FX20 controller instance
            hs_mux: High-speed mux controller
        """
        self._fx20 = fx20_controller
        self._hs_mux = hs_mux
        self._current_speed: Optional[USBSpeed] = None
        
    def set_speed(self, speed: USBSpeed) -> bool:
        """
        Set USB native speed configuration.
        
        Must be called BEFORE hotplug event for pre-connect speed setting.
        
        Args:
            speed: Target speed from USBSpeed enum
            
        Returns:
            True if speed set successfully
            
        Example:
            # Set USB to Gen1 x1 (5 Gbps, 1 lane)
            speed_ctrl.set_speed(USBSpeed.GEN1_X1)
        """
        try:
            # Ensure we're routed through FX20
            if self._hs_mux.get_path() != MuxPath.FX20_DIRECT:
                print("Warning: Enabling FX20 direct path for speed control")
                self._hs_mux.enable_br_bypass()
            
            # Configure FX20 for target speed
            self._fx20.set_link_speed(speed)
            self._current_speed = speed
            return True
        except Exception as e:
            print(f"Failed to set USB speed: {e}")
            return False
            
    def get_speed(self) -> Optional[USBSpeed]:
        """Get current USB speed configuration."""
        return self._current_speed
        
    def downgrade_before_connect(self, speed: USBSpeed) -> bool:
        """
        Configure downgraded speed before device connection.
        
        This addresses the requirement:
        "Support downgrade before the hotplug event"
        
        Args:
            speed: Target downgraded speed
            
        Returns:
            True if configured successfully
        """
        return self.set_speed(speed)
        
    def downgrade_with_reset(self, speed: USBSpeed) -> bool:
        """
        Downgrade speed with device reset/re-enumeration.
        
        This addresses the requirement:
        "Support downgrade after the hotplug event 
        (requiring a reset/re-enumeration)"
        
        Args:
            speed: Target downgraded speed
            
        Returns:
            True if downgrade successful
        """
        try:
            # Set target speed
            self._fx20.set_link_speed(speed)
            
            # Trigger USB reset for re-enumeration
            self._fx20.trigger_usb_reset()
            
            self._current_speed = speed
            return True
        except Exception as e:
            print(f"Failed to downgrade with reset: {e}")
            return False
