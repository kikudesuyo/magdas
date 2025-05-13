from datetime import date, datetime, timedelta

import numpy as np
from src.usecase.ee_index.calc.factory import EeFactory
from src.usecase.ee_index.calc.linear_completion import interpolate_nan
from src.usecase.ee_index.calc.moving_ave import calc_moving_avg
from src.usecase.ee_index.constant.eej import EEJ_THRESHOLD, EejDetectionTime
from src.usecase.ee_index.constant.magdas_station import EeIndexStation
from src.usecase.ee_index.helper.params import Period, StationParams
from src.usecase.kp import Kp


def calc_eej_peak_diff(
    dip_station: EeIndexStation, offdip_station: EeIndexStation, local_date: date
) -> float:
    start_ut = datetime(local_date.year, local_date.month, local_date.day, 0, 0)
    dip_eej_euel = calc_euel_for_eej_detection(dip_station, local_date)
    offdip_eej_euel = calc_euel_for_eej_detection(offdip_station, local_date)

    timestamp = np.array(
        [start_ut + timedelta(minutes=i) for i in range(len(dip_eej_euel))]
    )
    is_noon = np.array([EejDetectionTime.contains(dt.time()) for dt in timestamp])
    dip_max = np.max(dip_eej_euel[is_noon])
    offdip_max = np.max(offdip_eej_euel[is_noon])
    return dip_max - offdip_max


def calc_euel_for_eej_detection(station: EeIndexStation, local_date: date):
    s_lt = datetime(local_date.year, local_date.month, local_date.day, 0, 0)
    e_lt = s_lt.replace(hour=23, minute=59)
    lt_params = StationParams(station, Period(s_lt, e_lt))
    ut_params = lt_params.to_ut_params()

    factory = EeFactory()
    euel = factory.create_euel(ut_params)
    euel_values = euel.calc_euel()

    if not has_night_data(euel_values):
        return euel_values
    euel_for_baseline = np.concatenate(
        (
            euel_values[0 : 5 * 60],
            np.nan * np.ones(14 * 60),
            euel_values[19 * 60 : 24 * 60],
        )
    )
    y_filled = interpolate_nan(euel_for_baseline)
    euel_for_eej_detection = euel_values - y_filled
    return calc_moving_avg(euel_for_eej_detection, 60, 30)


def has_night_data(local_daily_data: np.ndarray) -> bool:
    """一日の夜間データが存在するかどうかを判定する"""
    if len(local_daily_data) != 1440:
        raise ValueError("daily_data must have 1440 elements.")
    dawn_e = local_daily_data[0 : 5 * 60]
    dusk_e = local_daily_data[19 * 60 : 24 * 60]
    return not (np.all(np.isnan(dawn_e)) and np.all(np.isnan(dusk_e)))


class EejDetection:
    def __init__(
        self,
        dip_station: EeIndexStation,
        offdip_station: EeIndexStation,
        target_date: date,
    ):
        if not dip_station.is_dip():
            raise ValueError("station is not in dip region")
        if not offdip_station.is_offdip():
            raise ValueError("station is not in dip region")

        factory = EeFactory()
        period = Period(
            datetime(target_date.year, target_date.month, target_date.day, 0, 0),
            datetime(target_date.year, target_date.month, target_date.day, 23, 59),
        )
        edst = factory.create_edst(period)
        self.min_edst = np.min(edst.calc_edst())
        self.kp = Kp().get_max(
            datetime(target_date.year, target_date.month, target_date.day, 0, 0),
            datetime(target_date.year, target_date.month, target_date.day, 23, 59),
        )
        self.eej_peak_diff = calc_eej_peak_diff(
            dip_station, offdip_station, target_date
        )

    def is_eej_present(self):
        return self.eej_peak_diff >= EEJ_THRESHOLD

    def is_singular_eej(self):
        if np.isnan(self.eej_peak_diff):
            return False
        # if self.kp < 4:
        #     return False
        # if self.min_edst < -30:
        #     return False

        if self.is_eej_present():
            return False
        return True


if __name__ == "__main__":
    import time

    log_s = time.time()

    anc = EeIndexStation.ANC
    eus = EeIndexStation.EUS
    d = date(2018, 1, 1)
    while d <= date(2018, 1, 31):
        eej = EejDetection(anc, eus, d)
        if eej.is_singular_eej():
            print(d)
            print(eej.eej_peak_diff)
        d += timedelta(days=1)
    log_e = time.time()
    print("log time: ", log_e - log_s)
