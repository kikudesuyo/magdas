from datetime import timedelta

import numpy as np
from src.constants.ee_index import MAX_ER, MIN_ER
from src.constants.time_relation import DawnAndDusk, TimeUnit
from src.usecase.ee_index.calc_h_component import HComponent
from src.usecase.ee_index.nan_calculator import NanCalculator
from src.utils.date import DateUtils


class Er:
    def __init__(self, h: HComponent):
        self.h = h
        self._er_values = None

    def calc_er(self, use_fixed_baseline: bool = True):
        """Calculate ER values.
        
        Args:
            use_fixed_baseline: If True, use the fixed baseline values from the CSV file.
                               If False, calculate the baseline from the current data.
        
        Returns:
            np.ndarray: The ER values.
        """
        # Cache the ER values to avoid recalculating them
        if self._er_values is not None:
            return self._er_values
            
        h_component = self.h.to_equatorial_h()
        
        if use_fixed_baseline:
            # Import here to avoid circular imports
            from src.usecase.ee_index.er_baseline import ErBaseline
            
            # Use the fixed baseline value from the CSV file
            base = ErBaseline.get_or_calculate_baseline(
                self.h.station, self.h.start_ut
            )
        else:
            # Calculate the baseline from the current data (original method)
            base = NanCalculator.nanmedian(h_component)
            
        raw_er = h_component - base
        self._er_values = self._remove_outliers(raw_er)
        return self._er_values

    def _remove_outliers(self, raw_er: np.ndarray) -> np.ndarray:
        raw_er[raw_er > MAX_ER] = np.nan
        raw_er[raw_er < MIN_ER] = np.nan
        return raw_er

    def _get_lt_array(self) -> np.ndarray:
        length = (
            int(
                (self.h.end_ut - self.h.start_ut).total_seconds()
                // TimeUnit.ONE_MINUTE.sec
            )
            + 1  # include start_ut
        )
        lt_arr = []
        for i in range(length):
            lt = DateUtils.to_lt(
                self.h.station, self.h.start_ut + timedelta(minutes=i)
            ).time()
            lt_arr.append(lt)
        return np.array(lt_arr)

    def nighttime_mask(self) -> np.ndarray:
        lt_arr = self._get_lt_array()
        return np.array([DawnAndDusk.NIGHTSIDE.contains(lt) for lt in lt_arr])

    def extract_night_er(self) -> np.ndarray:
        """Night definition 18:00 to 05:59"""
        night_er = np.where(
            self.nighttime_mask(),
            self.calc_er(),
            np.nan,
        )
        return night_er
