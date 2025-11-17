from datetime import datetime

import ephem
from src.constants.time_relation import MOON_CYCLE_DAYS


def get_lunar_age(ut: datetime) -> float:
    ephem_date = ephem.Date(ut)
    moon_age = ephem_date - ephem.previous_new_moon(ephem_date)
    return moon_age


# 月齢を24時間表記に換算した値を返す
def get_lunar_time(ut: datetime) -> float:
    moon_age = get_lunar_age(ut)
    lunar_hour = (moon_age / MOON_CYCLE_DAYS) * 24
    # 24時間表記に補正
    return lunar_hour % 24
