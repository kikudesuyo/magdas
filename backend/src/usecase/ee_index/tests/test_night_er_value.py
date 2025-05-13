import unittest
import warnings
from datetime import datetime, timedelta

import numpy as np
from src.constants.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.usecase.ee_index.calc_er import Er
from src.usecase.ee_index.calc_h_component import HComponent
from src.utils.date import DateUtils


class TestERValue(unittest.TestCase):
    """
    TODO: 夜側のERの値が1日ごとのベースラインによって求められているか確認する(未実施)
    """

    def setUp(self):
        warnings.filterwarnings(
            "ignore", category=RuntimeWarning, message="All-NaN slice encountered"
        )

    station = EeIndexStation.ANC
    start_ut = datetime(2014, 4, 1, 0, 0)
    end_ut = datetime(2014, 4, 2, 0, 0)

    def test_is_dayside_er_nan(self):
        """This function is a test code that checks whether the daytime values are set to np.NaN."""
        start_lt = DateUtils.to_lt(self.station, self.start_ut)
        end_lt = DateUtils.to_lt(self.station, self.end_ut)
        period = Period(start_lt, end_lt)
        p = StationParams(self.station, period)
        h = HComponent(p)
        er = Er(h)
        night_er = er.extract_night_er()

        current_time = start_lt
        i = 0
        while current_time <= end_lt:
            # 1分ごとに時間を進める
            if not er.nighttime_mask()[i]:
                err_msg = (
                    f"Error: 昼間側に値が存在します。index: {i}, 値: {night_er[i]}"
                )
                self.assertTrue(np.isnan(night_er[i]), err_msg)
            i += 1
            current_time += timedelta(minutes=1)
        print("Success!: 昼間側の値は全てnp.NaNです。in test_night_er_values.py")
