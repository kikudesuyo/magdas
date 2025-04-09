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


def calc_eej_value(
    dip_station: EeIndexStation, offdip_station: EeIndexStation, target_date: date
):
    start_dt = datetime(target_date.year, target_date.month, target_date.day, 0, 0)
    end_dt = start_dt + timedelta(days=1, minutes=-1)
    dip_euel = get_local_euel(dip_station, start_dt, end_dt)
    offdip_euel = get_local_euel(offdip_station, start_dt, end_dt)
    smoothed_dip_euel, smoothed_offdip_euel = (
        calc_moving_ave(dip_euel, 120, 60),
        calc_moving_ave(offdip_euel, 120, 60),
    )
    timestamp = np.array(
        [start_dt + timedelta(minutes=i) for i in range(len(smoothed_dip_euel))]
    )
    is_noon = np.array([EejDetectionTime.contains(dt.time()) for dt in timestamp])
    dip_max = np.max(smoothed_dip_euel[is_noon])
    offdip_max = np.max(smoothed_offdip_euel[is_noon])
    print(target_date)
    print(f"dip_max: {dip_max}, offdip_max: {offdip_max}")
    return dip_max - offdip_max


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
        self.eej_value = calc_eej_value(dip_station, offdip_station, target_date)

    def is_eej_present(self):
        return self.eej_value >= EEJ_THRESHOLD

    def is_singular_eej(self):
        if np.isnan(self.eej_value):
            return False
        # if self.kp < 4:
        #     return False
        # if self.min_edst < -30:
        #     return False

        if self.is_eej_present():
            return False
        return True


anc = EeIndexStation.ANC
eus = EeIndexStation.EUS
d = date(2014, 1, 1)
while d < date(2014, 1, 31):
    eej = EejDetection(anc, eus, d)
    if eej.is_singular_eej():
        print("singular eej")
        # print(d)
    d += timedelta(days=1)
