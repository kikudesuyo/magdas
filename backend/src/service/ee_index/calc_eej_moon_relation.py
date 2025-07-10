from datetime import datetime, timedelta

from matplotlib import pyplot as plt
from src.domain.magdas_station import EeIndexStation
from src.service.ee_index.calc_eej_detection import BestEuelSelectorForEej, EejDetection
from src.service.ee_index.calc_moon_phase import calc_moon_phase

anc = EeIndexStation.ANC
hua = EeIndexStation.HUA
eus = EeIndexStation.EUS

dip = [anc, hua]
offdip = [eus]

moon_pahse_d = {}  # key: moon_age, value([singular_eej_cnt, nan_cnt, total_cnt])

start_date = datetime(2017, 1, 1)
end_date = datetime(2020, 12, 31)


current = start_date
while current <= end_date:
    dip_euel_selector = BestEuelSelectorForEej(dip, current, is_dip=True)
    offdip_euel_selector = BestEuelSelectorForEej(offdip, current, is_dip=False)

    dip_euel = dip_euel_selector.select_euel_data()
    offdip_euel = offdip_euel_selector.select_euel_data()

    eej = EejDetection(dip_euel, offdip_euel, current.date())
    moon_age = int(calc_moon_phase(current))
    if moon_age not in moon_pahse_d:
        moon_pahse_d[moon_age] = [0, 0, 0]  # [singular_eej_cnt, nan_cnt, total_cnt]
    if eej.is_eej_peak_diff_nan():
        moon_pahse_d[moon_age][1] += 1
    if eej.is_singular_eej():
        moon_pahse_d[moon_age][0] += 1
    moon_pahse_d[moon_age][2] += 1
    current += timedelta(days=1)


moon_ages = sorted(moon_pahse_d.keys())

singular_rates = [
    moon_pahse_d[age][0] / moon_pahse_d[age][2] if moon_pahse_d[age][2] > 0 else 0
    for age in moon_ages
]


x = moon_ages
width = 0.4
fig, ax = plt.subplots(figsize=(12, 6))


plt.figure(figsize=(12, 6))
plt.bar(moon_ages, singular_rates, color="teal", alpha=0.7)
plt.xlabel("Moon Age (days)")
plt.ylabel("Singular EEJ Rate")
plt.title("Singular EEJ Rate by Moon Age")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()
