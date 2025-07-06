from datetime import datetime

import ephem


def calc_moon_phase(ut: datetime) -> float:
    ephem_date = ephem.Date(ut)
    moon_age = ephem_date - ephem.previous_new_moon(ephem_date)
    return moon_age
