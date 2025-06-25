import unittest
import warnings
from datetime import datetime

import numpy as np
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.service.ee_index.calc_er import Er
from src.service.ee_index.calc_h_component import HComponent
from src.utils.date import DateUtils


class TestERValue(unittest.TestCase):
    """
    TODO: 夜側のERの値が1日ごとのベースラインによって求められているか確認する(未実施)
    """

    station = EeIndexStation.ANC
    start_ut = datetime(2014, 4, 1, 0, 0)
    end_ut = datetime(2014, 4, 2, 0, 0)

    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            "ignore", category=RuntimeWarning, message="All-NaN slice encountered"
        )
        start_lt = DateUtils.to_lt(cls.station, cls.start_ut).replace(
            second=0, microsecond=0
        )
        end_lt = DateUtils.to_lt(cls.station, cls.end_ut).replace(
            second=0, microsecond=0
        )
        lt_period = Period(start_lt, end_lt)
        params = StationParams(cls.station, lt_period)
        h = HComponent(params)
        h_data = h.get_equatorial_h()
        cls.er = Er(h_data)
        cls.night_er = cls.er.extract_night_er()
        cls.night_mask = cls.er.nighttime_mask()

    def test_is_dayside_er_nan(self):
        """This function is a test code that checks whether the daytime values are set to np.NaN."""
        for i in range(len(self.night_er)):
            if not self.night_mask[i]:
                err_msg = (
                    f"Error: 昼間側に値が存在します。index: {i}, 値: {self.night_er[i]}"
                )
                self.assertTrue(np.isnan(self.night_er[i]), err_msg)
        print("Success!: 昼間側の値は全てnp.NaNです。in test_night_er_values.py")
