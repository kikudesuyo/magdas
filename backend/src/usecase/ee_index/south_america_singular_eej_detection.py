from datetime import timedelta

from src.domain.magdas_station import EeIndexStation
from src.service.ee_index.calc_eej_detection import BestEuelSelectorForEej, EejDetection
from src.utils.period import create_month_period

anc = EeIndexStation.ANC
hua = EeIndexStation.HUA
eus = EeIndexStation.EUS


dip = [anc, hua]
offdip = [eus]

year = 2015
# f = open("data/south_america_singular_eej.txt", "a")
f = open("data/test.txt", "a")
for year in range(2015, 2024):
    for month in range(1, 13):
        ut_period = create_month_period(year, month)
        start_date, end_date = (
            ut_period.start,
            ut_period.end,
        )
        current_date = start_date
        while current_date <= end_date:
            dip_euel_selector = BestEuelSelectorForEej(dip, current_date, is_dip=True)
            offdip_euel_selector = BestEuelSelectorForEej(
                offdip, current_date, is_dip=False
            )

            dip_euel = dip_euel_selector.select_euel_values()
            offdip_euel = offdip_euel_selector.select_euel_values()
            eej = EejDetection(dip_euel, offdip_euel, current_date.date())
            if eej.is_singular_eej():
                f.write(f"{current_date.date()}\n")
                print(f"southeast_asia_{current_date.date()}")
            current_date += timedelta(days=1)
        print("current_date:", current_date)
f.close()
