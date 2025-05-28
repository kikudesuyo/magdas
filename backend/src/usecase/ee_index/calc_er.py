import numpy as np
from numpy.typing import NDArray
from src.constants.ee_index import MAX_ER, MIN_ER
from src.constants.time_relation import DawnAndDusk, TimeUnit
from src.usecase.ee_index.calc_h_component import HData
from src.usecase.ee_index.nan_calculator import NanCalculator


class Er:
    def __init__(self, h_data: HData):
        self.h_data = h_data

    def calc_er(self):
        h_values = self.h_data.h_values
        base = NanCalculator.nanmedian(h_values)
        raw_er = h_values - base
        return self._remove_outliers(raw_er)

    def _remove_outliers(self, raw_er: np.ndarray) -> np.ndarray:
        filtered_er = np.where(
            (raw_er > MAX_ER) | (raw_er < MIN_ER),
            np.nan,
            raw_er,
        )
        return filtered_er

    def _get_lt_timestamps(self) -> NDArray[np.datetime64]:
        ut_timestamps = self.h_data.timestamps
        time_diff_hour = self.h_data.ut_params.station.time_diff
        time_diff_min = int(time_diff_hour * TimeUnit.ONE_HOUR.min)
        lt_timestamps = ut_timestamps + np.timedelta64(time_diff_min, "m")
        return np.array(lt_timestamps)

    def nighttime_mask(self) -> np.ndarray:
        lt_arr = self._get_lt_timestamps()
        lt_times = np.array(
            [lt.astype("datetime64[m]").astype("O").time() for lt in lt_arr]
        )
        return np.array([DawnAndDusk.NIGHTSIDE.contains(lt) for lt in lt_times])

    def extract_night_er(self) -> np.ndarray:
        """Night definition 18:00 to 05:59"""
        night_er = np.where(
            self.nighttime_mask(),
            self.calc_er(),
            np.nan,
        )
        return night_er
