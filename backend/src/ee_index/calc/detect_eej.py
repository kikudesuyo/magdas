from datetime import datetime, timedelta

from ee_index.calc.euel_index import Euel
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
