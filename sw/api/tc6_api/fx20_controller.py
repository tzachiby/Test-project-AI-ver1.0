"""
ThunderCat6 FX20 USB Traffic Generator Controller

TODO: Implement after obtaining FX20 datasheet from Infineon/Cypress
"""


class FX20Controller:
    """
    FX20 USB traffic generator controller.
    
    FX20 is selected to replace FX3 because it supports LPM
    (from TC6 requirements).
    
    TODO: Implement after obtaining:
    1. FX20 datasheet
    2. I2C register map
    3. SDK/programming guide
    """
    
    def __init__(self):
        # TODO: Implement after obtaining FX20 datasheet
        raise NotImplementedError("TODO: Obtain FX20 datasheet")
    
    def set_speed(self, speed: str):
        """
        Set USB speed.
        
        Required speeds (from TC6 requirements):
        - Gen1x1 (5 Gbps)
        - Gen1x2 (10 Gbps) 
        - Gen2x1 (10 Gbps)
        - Gen2x2 (20 Gbps)
        
        TODO: Implement from FX20 datasheet
        """
        raise NotImplementedError("TODO: Implement from FX20 datasheet")
    
    def set_lpm_state(self, state: str):
        """
        Set LPM (Link Power Management) state.
        
        LPM support is key reason for FX20 selection (from requirements).
        
        TODO: Implement from FX20 datasheet
        """
        raise NotImplementedError("TODO: Implement from FX20 datasheet")
    
    def start_traffic(self, pattern: str):
        """
        Start USB traffic pattern.
        
        Required patterns (from requirements):
        - Bulk
        - Interrupt
        - Isochronous In
        - Isochronous Out
        
        TODO: Implement from FX20 SDK
        """
        raise NotImplementedError("TODO: Implement from FX20 SDK")


# TODO: Define registers from FX20 datasheet
# TODO: Define I2C address from FX20 datasheet
# TODO: Define LPM states from FX20 datasheet
# TODO: Define traffic patterns from FX20 SDK
