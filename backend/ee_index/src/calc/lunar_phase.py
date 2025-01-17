from datetime import datetime

import ephem

moon = ephem.Moon()

moon.compute()
dt = datetime(2022, 1, 11).strftime("%Y/%m/%d %H:%M:%S")
ephem_date = ephem.Date(dt)
moon.compute(ephem_date)
moon_age = ephem_date - ephem.previous_new_moon(ephem_date)
print(f"Moon age: {moon_age} days")
