import unittest
import warnings
from datetime import datetime, timedelta

import numpy as np
from src.ee_index.calc.er_value import NightEr
from src.ee_index.constant.magdas_station import EeIndexStation
from src.ee_index.helper.time_utils import DateUtils


class TestERValue(unittest.TestCase):
    """
    TODO: 夜側のERの値が1日ごとのベースラインによって求められているか確認する(未実施)
    """

    def setUp(self):
        warnings.filterwarnings(
            "ignore", category=RuntimeWarning, message="All-NaN slice encountered"
        )

    station = "EUS"
    ut_date = datetime(2010, 4, 1)
    days = 3

    def test_is_dayside_er_nan(self):
        """This function is a test code that checks whether the daytime values are set to np.NaN."""
        local_start_dt = DateUtils.to_local_time(self.station, self.ut_date)
        local_end_dt = local_start_dt + timedelta(days=self.days, minutes=-1)
        nightside = NightEr(self.station, local_start_dt, local_end_dt)
        nightside_er = nightside.extract_night_er()
        # onset time is dayside
        time_zone = EeIndexStation[self.station].time_diff
        if time_zone < -6:
            nightside_start_index = (abs(time_zone) - 6) * 60
            nightside_end_index = nightside_start_index + 12 * 60 - 1
            i = 0
            while True:
                if i < nightside_start_index or i > nightside_end_index:
                    self.assertTrue(
                        np.isnan(nightside_er[i]), "Error: 昼間側に値がある"
                    )
                i += 1
                if i == 1440:
                    break
        elif -6 <= time_zone < 0:
            nightside_end_index = (abs(time_zone) + 6) * 60 - 1
            nightside_start_index = nightside_end_index + 12 * 60 + 1
            i = 0
            while True:
                if nightside_end_index < i < nightside_start_index:
                    self.assertTrue(
                        np.isnan(nightside_er[i]), "Error: 昼間側に値がある"
                    )
                i += 1
                if i == 1440:
                    break
        elif 0 <= time_zone < 6:
            nightside_end_index = (abs(time_zone)) * 60 - 1
            nightside_start_index = nightside_end_index + 12 * 60 + 1
            i = 0
            while True:
                if nightside_end_index < i < nightside_start_index:
                    self.assertTrue(np.isnan(nightside_er[i]), "Error:昼間側に値がある")
                i += 1
                if i == 1440:
                    break
        elif 6 <= time_zone:
            nightside_start_index = (18 - abs(time_zone)) * 60
            nightside_end_index = nightside_start_index + 12 * 60 - 1
            i = 0
            while True:
                if i < nightside_start_index or i > nightside_end_index:
                    self.assertTrue(np.isnan(nightside_er[i]), "Error:昼間側に値がある")
                i += 1
                if i == 1440:
                    break
        print("Success!: 昼間側の値は全てnp.NaNです。in test_night_er_values.py")
