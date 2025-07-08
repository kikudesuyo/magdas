from datetime import datetime

from src.dev.save_singular_eej import write_singular_eej_to_csv
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period

anc = EeIndexStation.ANC
hua = EeIndexStation.HUA
eus = EeIndexStation.EUS


dip = [anc, hua]
offdip = [eus]

year = 2015


period = Period(start=datetime(2015, 1, 1), end=datetime(2023, 12, 31))


write_singular_eej_to_csv(
    period,
    dip_stations=dip,
    offdip_stations=offdip,
    path="data/southeast_asia_singular_eej.csv",
)
