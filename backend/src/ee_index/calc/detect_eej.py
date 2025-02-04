from datetime import datetime, timedelta

import numpy as np
from ee_index.calc.euel_index import Euel
from ee_index.constant.eej import EEJ_THRESHOLD, EejDetectionTime
from ee_index.constant.magdas_station import EeIndexStation


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


def is_eej_present(
    equatorial_station, dip_station, local_start_dt: datetime, local_end_dt: datetime
):
    # TODO: ピークtoピークを比較するべき。
    # 例えば11時とかのピークじゃないところで50nT以上があった場合にEEJと判定するのはおかしい
    if not is_equatorial_station(equatorial_station):
        raise ValueError("Equatorial station is not in equatorial region")
    if not is_dip_station(dip_station):
        raise ValueError("Dip station is not in dip region")
    equatorial_euel = get_local_euel(equatorial_station, local_start_dt, local_end_dt)
    dip_euel = get_local_euel(dip_station, local_start_dt, local_end_dt)
    euel_diff = equatorial_euel - dip_euel
    time_stamp = np.array(
        [local_start_dt + timedelta(minutes=i) for i in range(len(euel_diff))]
    )
    start_time = EejDetectionTime.START
    end_time = EejDetectionTime.END
    is_noon = np.array(
        [start_time <= dt.time() <= end_time for dt in time_stamp], dtype=bool
    )
    is_eej_present = any(is_noon & (euel_diff > EEJ_THRESHOLD))
    return is_eej_present
