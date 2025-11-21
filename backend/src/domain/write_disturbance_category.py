import csv
from datetime import date, datetime, timedelta

import numpy as np
from src.domain.station_params import Period
from src.service.calc_eej_detection import DisturbanceCategory
from src.service.ee_index.factory_ee import EeFactory
from src.service.kp import Kp


def calc_daily_min_edst(local_date: date):
    s_dt = datetime(local_date.year, local_date.month, local_date.day, 0, 0)
    e_dt = s_dt.replace(hour=23, minute=59)
    period = Period(s_dt, e_dt)
    factory = EeFactory()
    edst = factory.create_edst(period)
    return np.min(edst.calc_edst())


start = datetime(2022, 12, 31)
end = datetime(2022, 12, 31)

OUTPUT_FILE_PATH = "eej_category_results.csv"


kp = Kp()
current_date = start

with open(OUTPUT_FILE_PATH, "a", newline="", buffering=1) as f:
    writer = csv.writer(f)
    writer.writerow(["date", "min_edst", "max_kp", "category"])

    while current_date <= end:
        min_edst = calc_daily_min_edst(current_date)
        ut_period = Period(
            datetime(current_date.year, current_date.month, current_date.day, 0, 0),
            datetime(current_date.year, current_date.month, current_date.day, 23, 59),
        )

        max_kp = Kp().get_max_of_day(ut_period)
        eej_category = DisturbanceCategory.from_conditions(
            daily_max_kp=max_kp, daily_min_edst=min_edst
        )
        writer.writerow(
            [
                current_date.strftime("%Y-%m-%d"),
                min_edst,
                max_kp,
                eej_category.label,
            ]
        )
        current_date += timedelta(days=1)

print(f"Successfully exported to {OUTPUT_FILE_PATH}")
