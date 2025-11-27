from datetime import datetime

import ephem
from src.constants.time_relation import MOON_CYCLE_DAYS


def get_lunar_date(ut: datetime) -> float:
    ephem_date = ephem.Date(ut)
    moon_date = ephem_date - ephem.previous_new_moon(ephem_date)
    return moon_date


# 月齢を24時間表記に換算した値を返す
def get_lunar_age(ut: datetime) -> float:
    moon_date = get_lunar_date(ut)
    lunar_hour = (moon_date / MOON_CYCLE_DAYS) * 24
    # 24時間表記に補正
    return lunar_hour % 24
