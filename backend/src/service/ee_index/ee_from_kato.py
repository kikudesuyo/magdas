import csv
from datetime import datetime, timedelta

import numpy as np
from domain.station_params import Period
from src.repository.ee_from_kato import KatoEeData, KatoEeRepository
from src.service.calc_eej_detection import EejDetection


class EeFromKatoService:
    def __init__(self, station_code: str):
        self.repository = KatoEeRepository(station_code)

    def get_ee_data_by_range(self, period: Period) -> list[KatoEeData]:
        return self.repository.select_by_range(period)


period = Period(
    start=datetime(2016, 1, 1),
    end=datetime(2016, 12, 31, 23, 59),
)

dip_data = EeFromKatoService("TTB").get_ee_data_by_range(period)
dip_euel_data = np.array([d.euel_data for d in dip_data])
dip_euel_chunks = np.array_split(dip_euel_data, len(dip_euel_data) // 1440)


offdip_data = [
    EeFromKatoService("KOU").get_ee_data_by_range(period),
    EeFromKatoService("EUS").get_ee_data_by_range(period),
]


offdip_euel_data = [np.array([d.euel_data for d in data]) for data in offdip_data]
offdip_euel_chunks = [
    np.array_split(data, len(data) // 1440) for data in offdip_euel_data
]


start_date = datetime(2016, 1, 1)
end_date = datetime(2020, 12, 31)

output_file = (
    "/Users/kiku/directory/dev/magdas/backend/src/service/ee_index/eej_results.csv"
)


# with open(output_file, mode="w", newline="") as file:
#     writer = csv.writer(file)
#     writer.writerow(["Date", "Category", "Diff"])

#     current_date = start_date
#     while current_date <= end_date:
#         day_index = (current_date - start_date).days
#         offdip_day_chunks = [
#             chunks[day_index][540:900] for chunks in offdip_euel_chunks
#         ]

#         dip_day_chunk = dip_euel_chunks[day_index][540:900]
#         best_offdip_day_data = min(
#             offdip_day_chunks, key=lambda chunk: np.isnan(chunk).mean()
#         )

#         dip_max = np.max(dip_day_chunk)
#         offdip_max = np.max(best_offdip_day_data)
#         peak_diff = dip_max - offdip_max
#         eej = EejDetection(peak_diff, current_date)
#         category = eej.classify_eej_category()
#         print(current_date, category, peak_diff)
#         writer.writerow([current_date.date(), category.label, peak_diff])

#         current_date += timedelta(days=1)
