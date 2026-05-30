"""
ThunderCat6 Gen T (PCIe Tunneling) Controller API

Provides control and monitoring of PCIe tunneling through USB4/TBT connection.
Supports bandwidth testing, hot plug, and link diagnostics.
"""

import logging
from typing import Dict, Optional, Tuple
from enum import Enum, auto
from dataclasses import dataclass
import time

logger = logging.getLogger(__name__)


class PCIeSpeed(Enum):
    """PCIe link speed"""
    GEN1 = 1  # 2.5GT/s
    GEN2 = 2  # 5GT/s
    GEN3 = 3  # 8GT/s
    GEN4 = 4  # 16GT/s


class PCIeWidth(Enum):
    """PCIe link width"""
    X1 = 1
    X2 = 2
    X4 = 4


class LTSSMState(Enum):
    """PCIe LTSSM state"""
    DETECT = auto()
    POLLING = auto()
    CONFIG = auto()
    L0 = auto()        # Active
    L0s = auto()       # Low power standby
    L1 = auto()        # Low power
    L2 = auto()        # Deeper low power
    RECOVERY = auto()
    DISABLED = auto()
    LOOPBACK = auto()
    HOT_RESET = auto()


class GenTMode(Enum):
    """Gen T operation modes"""
    PCIE_X4 = 0x8       # Full PCIe Gen4 x4
    PCIE_X2 = 0x9       # Reduced PCIe Gen4 x2
    PCIE_X1 = 0xA       # Minimal PCIe Gen4 x1
    PCIE_PLUS_DP = 0xB  # PCIe + DP Alt Mode
    BANDWIDTH = 0xC     # Bandwidth stress test


@dataclass
class PCIeTunnelStatus:
    """PCIe tunnel status information"""
    link_up: bool
    width: PCIeWidth
    speed: PCIeSpeed
    ltssm_state: LTSSMState
    error_count: int
    recovery_count: int
    correctable_errors: int
    uncorrectable_errors: int


@dataclass
class BandwidthStats:
    """Bandwidth statistics"""
    tx_bandwidth_mbps: float
    rx_bandwidth_mbps: float
    tx_utilization_pct: float
    rx_utilization_pct: float


@dataclass
class SSDInfo:
    """NVMe SSD information"""
    model: str
    serial: str
    firmware: str
    capacity_gb: int
    temperature_c: int
    health_pct: int


@dataclass
class BenchmarkResult:
    """SSD benchmark results"""
    seq_read_mbps: float
    seq_write_mbps: float
    rand_4k_read_iops: int
    rand_4k_write_iops: int
    latency_avg_us: float
    latency_p99_us: float


class GenTController:
    """
    Gen T (PCIe Tunneling) Controller for ThunderCat6
    
    Manages PCIe tunnel through USB4/Thunderbolt connection,
    including SSD access, bandwidth testing, and diagnostics.
    """
    
    # I2C register addresses for Gen T
    PCIE_CTRL = 0x40
    PCIE_STATUS = 0x41
    PCIE_WIDTH = 0x42
    PCIE_SPEED = 0x43
    PCIE_ERR_CNT = 0x44
    PCIE_RCV_CNT = 0x45
    PCIE_CORR_ERR = 0x46
    PCIE_UNCORR_ERR = 0x47
    PCIE_BW_TX = 0x48
    PCIE_BW_RX = 0x49
    PCIE_LTSSM = 0x4A
    PCIE_INJECT = 0x4B
    
    # Control bits
    CTRL_ENABLE = 0x01
    CTRL_FORCE_WIDTH = 0x02
    CTRL_FORCE_SPEED = 0x04
    CTRL_HOT_PLUG = 0x08
    CTRL_PM_DISABLE = 0x10
    CTRL_ERROR_INJECT = 0x20
    
    def __init__(self, i2c_interface=None):
        """
        Initialize Gen T Controller
        
        Args:
            i2c_interface: I2C communication interface (e.g., from FTDI)
        """
        self._i2c = i2c_interface
        self._connected = False
        self._current_mode = None
        self._ssd_info: Optional[SSDInfo] = None
        
    def connect(self, i2c_interface=None) -> bool:
        """
        Connect to Gen T controller
        
        Args:
            i2c_interface: Optional I2C interface to use
            
        Returns:
            True if connection successful
        """
        if i2c_interface:
            self._i2c = i2c_interface
            
        if not self._i2c:
            logger.error("No I2C interface provided")
            return False
            
        self._connected = True
        logger.info("Gen T controller connected")
        return True
        
    def disconnect(self):
        """Disconnect from Gen T controller"""
        if self._ssd_info:
            self.safe_eject_ssd()
        self._connected = False
        logger.info("Gen T controller disconnected")
        
    def set_mode(self, mode: GenTMode) -> bool:
        """
        Set Gen T operation mode
        
        Args:
            mode: GenTMode enum value
            
        Returns:
            True if mode set successfully
        """
        if not self._connected:
            raise RuntimeError("Not connected")
            
        logger.info(f"Setting Gen T mode: {mode.name}")
        
        # Configure based on mode
        if mode == GenTMode.PCIE_X4:
            self._set_pcie_width(PCIeWidth.X4)
            self._set_pcie_speed(PCIeSpeed.GEN4)
        elif mode == GenTMode.PCIE_X2:
            self._set_pcie_width(PCIeWidth.X2)
            self._set_pcie_speed(PCIeSpeed.GEN4)
        elif mode == GenTMode.PCIE_X1:
            self._set_pcie_width(PCIeWidth.X1)
            self._set_pcie_speed(PCIeSpeed.GEN4)
        elif mode == GenTMode.PCIE_PLUS_DP:
            self._set_pcie_width(PCIeWidth.X2)  # Reduced for DP sharing
            self._set_pcie_speed(PCIeSpeed.GEN4)
        elif mode == GenTMode.BANDWIDTH:
            self._set_pcie_width(PCIeWidth.X4)
            self._set_pcie_speed(PCIeSpeed.GEN4)
            self._disable_power_management()
            
        self._current_mode = mode
        return True
        
    def _set_pcie_width(self, width: PCIeWidth):
        """Set PCIe link width"""
        if self._i2c:
            self._i2c.write_register(self.PCIE_WIDTH, width.value)
            ctrl = self._i2c.read_register(self.PCIE_CTRL)
            self._i2c.write_register(self.PCIE_CTRL, ctrl | self.CTRL_FORCE_WIDTH)
            
    def _set_pcie_speed(self, speed: PCIeSpeed):
        """Set PCIe link speed"""
        if self._i2c:
            self._i2c.write_register(self.PCIE_SPEED, speed.value)
            ctrl = self._i2c.read_register(self.PCIE_CTRL)
            self._i2c.write_register(self.PCIE_CTRL, ctrl | self.CTRL_FORCE_SPEED)
            
    def _disable_power_management(self):
        """Disable PCIe power management for stress testing"""
        if self._i2c:
            ctrl = self._i2c.read_register(self.PCIE_CTRL)
            self._i2c.write_register(self.PCIE_CTRL, ctrl | self.CTRL_PM_DISABLE)
            
    def get_tunnel_status(self) -> PCIeTunnelStatus:
        """
        Get PCIe tunnel status
        
        Returns:
            PCIeTunnelStatus with current link state
        """
        if not self._connected:
            raise RuntimeError("Not connected")
            
        if self._i2c:
            status = self._i2c.read_register(self.PCIE_STATUS)
            width = self._i2c.read_register(self.PCIE_WIDTH)
            speed = self._i2c.read_register(self.PCIE_SPEED)
            ltssm = self._i2c.read_register(self.PCIE_LTSSM)
            err_cnt = self._i2c.read_register(self.PCIE_ERR_CNT)
            rcv_cnt = self._i2c.read_register(self.PCIE_RCV_CNT)
            corr_err = self._i2c.read_register(self.PCIE_CORR_ERR)
            uncorr_err = self._i2c.read_register(self.PCIE_UNCORR_ERR)
            
            return PCIeTunnelStatus(
                link_up=(status & 0x01) != 0,
                width=PCIeWidth(width) if width in [1, 2, 4] else PCIeWidth.X1,
                speed=PCIeSpeed(speed) if speed in [1, 2, 3, 4] else PCIeSpeed.GEN1,
                ltssm_state=LTSSMState.L0 if (status & 0x01) else LTSSMState.DETECT,
                error_count=err_cnt,
                recovery_count=rcv_cnt,
                correctable_errors=corr_err,
                uncorrectable_errors=uncorr_err
            )
        else:
            # Simulation mode
            return PCIeTunnelStatus(
                link_up=True,
                width=PCIeWidth.X4,
                speed=PCIeSpeed.GEN4,
                ltssm_state=LTSSMState.L0,
                error_count=0,
                recovery_count=0,
                correctable_errors=0,
                uncorrectable_errors=0
            )
            
    def get_bandwidth_stats(self) -> BandwidthStats:
        """
        Get real-time bandwidth statistics
        
        Returns:
            BandwidthStats with current bandwidth usage
        """
        if not self._connected:
            raise RuntimeError("Not connected")
            
        if self._i2c:
            tx_bw = self._i2c.read_register(self.PCIE_BW_TX) * 100  # 100MB/s units
            rx_bw = self._i2c.read_register(self.PCIE_BW_RX) * 100
            
            # Max theoretical bandwidth for Gen4 x4 = ~7GB/s each direction
            max_bw = 7000
            
            return BandwidthStats(
                tx_bandwidth_mbps=tx_bw,
                rx_bandwidth_mbps=rx_bw,
                tx_utilization_pct=(tx_bw / max_bw) * 100,
                rx_utilization_pct=(rx_bw / max_bw) * 100
            )
        else:
            # Simulation mode
            return BandwidthStats(
                tx_bandwidth_mbps=3500,
                rx_bandwidth_mbps=3000,
                tx_utilization_pct=50,
                rx_utilization_pct=43
            )
            
    def check_ssd_enumerated(self) -> bool:
        """
        Check if NVMe SSD is enumerated on host
        
        Returns:
            True if SSD is visible to host OS
        """
        if not self._connected:
            raise RuntimeError("Not connected")
            
        status = self.get_tunnel_status()
        return status.link_up and status.ltssm_state == LTSSMState.L0
        
    def get_ssd_info(self) -> Optional[SSDInfo]:
        """
        Get NVMe SSD information
        
        Returns:
            SSDInfo or None if not available
        """
        if not self.check_ssd_enumerated():
            return None
            
        # In real implementation, query via NVMe admin commands
        # For now, return cached/simulated info
        return SSDInfo(
            model="Samsung 980 PRO",
            serial="S5GXNF0R123456",
            firmware="5B2QGXA7",
            capacity_gb=512,
            temperature_c=45,
            health_pct=100
        )
        
    def run_benchmark(self, 
                      test_size_gb: int = 1,
                      queue_depth: int = 32,
                      num_jobs: int = 4) -> BenchmarkResult:
        """
        Run SSD benchmark through PCIe tunnel
        
        Args:
            test_size_gb: Test data size in GB
            queue_depth: I/O queue depth
            num_jobs: Number of parallel jobs
            
        Returns:
            BenchmarkResult with performance metrics
        """
        if not self._connected:
            raise RuntimeError("Not connected")
            
        if not self.check_ssd_enumerated():
            raise RuntimeError("SSD not enumerated")
            
        logger.info(f"Running benchmark: {test_size_gb}GB, QD={queue_depth}, jobs={num_jobs}")
        
        # In real implementation, use fio or similar tool
        # For now, return expected values based on tunnel bandwidth
        
        status = self.get_tunnel_status()
        
        # Calculate expected bandwidth based on width/speed
        width_factor = status.width.value / 4
        speed_factor = status.speed.value / 4
        
        base_read = 7000   # 7GB/s for Gen4 x4
        base_write = 5000  # 5GB/s for Gen4 x4
        
        # Tunnel overhead ~10%
        tunnel_efficiency = 0.9
        
        return BenchmarkResult(
            seq_read_mbps=base_read * width_factor * speed_factor * tunnel_efficiency,
            seq_write_mbps=base_write * width_factor * speed_factor * tunnel_efficiency,
            rand_4k_read_iops=int(700000 * width_factor * speed_factor),
            rand_4k_write_iops=int(500000 * width_factor * speed_factor),
            latency_avg_us=15.0 / (width_factor * speed_factor),
            latency_p99_us=50.0 / (width_factor * speed_factor)
        )
        
    def safe_eject_ssd(self) -> bool:
        """
        Safely eject SSD before disconnect
        
        Returns:
            True if ejection successful
        """
        if not self._connected:
            return False
            
        logger.info("Safely ejecting SSD...")
        
        # Flush caches and prepare for removal
        # In real implementation, send NVMe flush/shutdown
        
        self._ssd_info = None
        return True
        
    def inject_link_error(self, count: int = 1) -> int:
        """
        Inject PCIe link errors for recovery testing
        
        Args:
            count: Number of errors to inject
            
        Returns:
            Number of errors successfully injected
        """
        if not self._connected:
            raise RuntimeError("Not connected")
            
        logger.warning(f"Injecting {count} link errors")
        
        if self._i2c:
            # Enable error injection and set count
            ctrl = self._i2c.read_register(self.PCIE_CTRL)
            self._i2c.write_register(self.PCIE_INJECT, count)
            self._i2c.write_register(self.PCIE_CTRL, ctrl | self.CTRL_ERROR_INJECT)
            
        return count
        
    def wait_for_link_recovery(self, timeout_sec: float = 5.0) -> bool:
        """
        Wait for link to recover after error injection
        
        Args:
            timeout_sec: Maximum time to wait
            
        Returns:
            True if link recovered within timeout
        """
        start = time.time()
        
        while time.time() - start < timeout_sec:
            status = self.get_tunnel_status()
            if status.link_up and status.ltssm_state == LTSSMState.L0:
                return True
            time.sleep(0.1)
            
        return False
        
    def clear_error_counters(self):
        """Clear all PCIe error counters"""
        if self._i2c:
            self._i2c.write_register(self.PCIE_ERR_CNT, 0)
            self._i2c.write_register(self.PCIE_RCV_CNT, 0)
            self._i2c.write_register(self.PCIE_CORR_ERR, 0)
            self._i2c.write_register(self.PCIE_UNCORR_ERR, 0)
            
    def get_error_count(self) -> int:
        """Get total error count"""
        status = self.get_tunnel_status()
        return status.error_count + status.correctable_errors + status.uncorrectable_errors


# Convenience functions
def test_gen_t_basic():
    """Basic Gen T connectivity test"""
    ctrl = GenTController()
    ctrl.connect()
    ctrl.set_mode(GenTMode.PCIE_X4)
    
    status = ctrl.get_tunnel_status()
    print(f"Link Up: {status.link_up}")
    print(f"Width: x{status.width.value}")
    print(f"Speed: Gen{status.speed.value}")
    
    if status.link_up:
        bw = ctrl.get_bandwidth_stats()
        print(f"TX: {bw.tx_bandwidth_mbps} MB/s ({bw.tx_utilization_pct:.1f}%)")
        print(f"RX: {bw.rx_bandwidth_mbps} MB/s ({bw.rx_utilization_pct:.1f}%)")
        
    ctrl.disconnect()
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_gen_t_basic()
