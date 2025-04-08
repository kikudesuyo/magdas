from datetime import datetime

import ephem


def calc_moon_phase(dt: datetime) -> float:
    moon = ephem.Moon()
    moon.compute()
    ephem_date = ephem.Date(dt)
    moon.compute(ephem_date)
    moon_age = ephem_date - ephem.previous_new_moon(ephem_date)
    return moon_age
