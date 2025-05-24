import numpy as np
from src.domain.station_params import Period, StationParams
from src.usecase.ee_index.calc_edst import Edst
from src.usecase.ee_index.calc_er import Er


class Euel:
    def __init__(self, er: Er, edst: Edst):
        self.er = er
        self.edst = edst
        self._euel_values = None

    def calc_euel(self, adjust_nighttime: bool = True) -> np.ndarray:
        """Calculate EUEL values.
        
        Args:
            adjust_nighttime: If True, adjust the EUEL values so that nighttime values
                             are closer to 0.
        
        Returns:
            np.ndarray: The EUEL values.
        """
        # Cache the EUEL values to avoid recalculating them
        if self._euel_values is not None:
            return self._euel_values
            
        # Calculate EUEL values
        euel_values = self.er.calc_er() - self.edst.calc_edst()
        
        if adjust_nighttime:
            # Import here to avoid circular imports
            from src.usecase.ee_index.er_baseline import ErBaseline
            
            # Get the station and period from the ER object
            station = self.er.h.station
            period = self.er.h.period if hasattr(self.er.h, 'period') else Period(self.er.h.start_ut, self.er.h.end_ut)
            
            # Calculate the offset to apply to EUEL values
            offset = ErBaseline.get_night_euel_offset(station, period)
            
            # Apply the offset
            euel_values = euel_values - offset
        
        self._euel_values = euel_values
        return self._euel_values
