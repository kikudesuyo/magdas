from datetime import date, datetime, timedelta

import numpy as np
from ee_index.calc.euel_index import Euel
from ee_index.constant.eej import EEJ_THRESHOLD, EejDetectionTime
from ee_index.constant.magdas_station import EeIndexStation
from matplotlib import pyplot as plt
from src.ee_index.calc.moving_ave import calc_moving_ave


def get_local_euel(station: EeIndexStation, local_start_dt: datetime, local_end_dt):
    start_utc = (local_start_dt - timedelta(hours=station.time_diff)).replace(
        second=0, microsecond=0
    )
    end_utc = (local_end_dt - timedelta(hours=station.time_diff)).replace(
        second=0, microsecond=0
    )
    euel = Euel.calc_euel(station.code, start_utc, end_utc)
    return euel


def is_equatorial_station(station: EeIndexStation):
    return -3 < station.gm_lat < 3


def is_dip_station(station: EeIndexStation):
    return 3 <= abs(station.gm_lat) <= 15


def is_eej_present(equatorial_station, dip_station, date: date):
    # TODO: ピークtoピークを比較するべき。
    # 例えば11時とかのピークじゃないところで50nT以上があった場合にEEJと判定するのはおかしい
    if not is_equatorial_station(equatorial_station):
        raise ValueError("Equatorial station is not in equatorial region")
    if not is_dip_station(dip_station):
        raise ValueError("Dip station is not in dip region")

    start_dt = datetime(date.year, date.month, date.day, 0, 0)
    end_dt = start_dt + timedelta(days=1, minutes=-1)
    dip_euel = get_local_euel(equatorial_station, start_dt, end_dt)
    off_dip_euel = get_local_euel(dip_station, start_dt, end_dt)
    smoothed_dip_euel = calc_moving_ave(dip_euel, 120, 60)
    smoothed_off_dip_euel = calc_moving_ave(off_dip_euel, 120, 60)
    time_stamp = np.array(
        [start_dt + timedelta(minutes=i) for i in range(len(smoothed_dip_euel))]
    )
    is_noon = np.array(
        [
            EejDetectionTime.START <= dt.time() <= EejDetectionTime.END
            for dt in time_stamp
        ]
    )
    dip_max = np.max(smoothed_dip_euel[is_noon])
    off_dip_max = np.max(smoothed_off_dip_euel[is_noon])
    return dip_max - off_dip_max >= EEJ_THRESHOLD
