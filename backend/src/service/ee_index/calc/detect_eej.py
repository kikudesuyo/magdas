from datetime import date, datetime, timedelta

import numpy as np
from src.service.ee_index.calc.edst_index import Edst
from src.service.ee_index.calc.euel_index import get_local_euel
from src.service.ee_index.calc.moving_ave import calc_moving_ave
from src.service.ee_index.constant.eej import EEJ_THRESHOLD, EejDetectionTime
from src.service.ee_index.constant.magdas_station import EeIndexStation
from src.service.kp import Kp


def is_dip_station(station: EeIndexStation):
    return abs(station.gm_lat) < 3


def is_offdip_station(station: EeIndexStation):
    return 3 <= abs(station.gm_lat) <= 15


def calc_eej_peak_diff(
    dip_station: EeIndexStation, offdip_station: EeIndexStation, local_date: date
):
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
    euel = get_local_euel(station, s_lt, e_lt)
    dawn_e = np.array(euel[0 : 5 * 60])
    dayside_nan = np.nan * np.ones(14 * 60)
    dusk_e = np.array(euel[19 * 60 : 24 * 60])
    if np.all(np.isnan(dawn_e)) and np.all(np.isnan(dusk_e)):
        return euel

    euel_for_baseline = np.concatenate((dawn_e, dayside_nan, dusk_e))
    # NaNの補間
    x = np.arange(len(euel_for_baseline))
    nan_indices = np.isnan(euel_for_baseline)
    x_valid = x[~nan_indices]
    y_valid = euel_for_baseline[~nan_indices]
    y_filled = euel_for_baseline.copy()
    y_filled[nan_indices] = np.interp(x[nan_indices], x_valid, y_valid)

    # 補間されたベースラインとの差分
    euel_for_eej_detection = euel - y_filled
    return calc_moving_ave(euel_for_eej_detection, 60, 30)


class EejDetection:
    def __init__(
        self,
        dip_station: EeIndexStation,
        offdip_station: EeIndexStation,
        target_date: date,
    ):
        if not is_dip_station(dip_station):
            raise ValueError("station is not in dip region")
        if not is_offdip_station(offdip_station):
            raise ValueError("station is not in off dip region")
        edst_val = Edst.compute_smoothed_edst(
            datetime(target_date.year, target_date.month, target_date.day, 0, 0),
            datetime(target_date.year, target_date.month, target_date.day, 23, 59),
        )
        self.min_edst = np.min(edst_val)
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
    anc = EeIndexStation.ANC
    eus = EeIndexStation.EUS
    d = date(2014, 1, 1)
    while d <= date(2014, 1, 5):
        eej = EejDetection(anc, eus, d)
        if eej.is_singular_eej():
            print("singular eej")
            print(d)
        d += timedelta(days=1)
