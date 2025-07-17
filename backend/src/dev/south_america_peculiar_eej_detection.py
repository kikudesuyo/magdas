from datetime import datetime

from src.dev.write_peculiar_eej import (
    write_eej_category_to_csv,
    write_peculiar_eej_to_csv,
)
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period

anc = EeIndexStation.ANC
hua = EeIndexStation.HUA
eus = EeIndexStation.EUS


dips = [anc, hua]
offdips = [eus]

year = 2015


period = Period(start=datetime(2014, 1, 1), end=datetime(2020, 12, 31))


# write_peculiar_eej_to_csv(
#     period,
#     dip_stations=dips,
#     offdip_stations=offdips,
#     path="data/south_america_peculiar_eej.csv",
# )

write_eej_category_to_csv(
    period,
    dip_stations=dips,
    offdip_stations=offdips,
    path="data/t.csv",
)
