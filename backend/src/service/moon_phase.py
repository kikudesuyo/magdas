from datetime import datetime

import ephem

MOON_CYCLE_DAYS = 29.53058867


def get_lunar_age(ut: datetime) -> float:
    ephem_date = ephem.Date(ut)
    moon_age = ephem_date - ephem.previous_new_moon(ephem_date)
    return moon_age


# 月齢を24時間表記に換算した値を返す
def get_lunar_time(ut: datetime) -> float:
    ephem_date = ephem.Date(ut)
    moon_age = ephem_date - ephem.previous_new_moon(ephem_date)
    return (moon_age / MOON_CYCLE_DAYS) * 24
