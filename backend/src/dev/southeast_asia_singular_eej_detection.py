from datetime import datetime

from src.dev.save_singular_eej import write_singular_eej_to_csv
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period

# ama = EeIndexStation.AMA
bcl = EeIndexStation.BCL
# bkl = EeIndexStation.BKL
cdo = EeIndexStation.CDO
ceb = EeIndexStation.CEB
dav = EeIndexStation.DAV
# daw = EeIndexStation.DAW
gsi = EeIndexStation.GSI
# hln = EeIndexStation.HLN
lgz = EeIndexStation.LGZ
lkw = EeIndexStation.LKW
lwa = EeIndexStation.LWA
mnd = EeIndexStation.MND
mut = EeIndexStation.MUT
scn = EeIndexStation.SCN
tgg = EeIndexStation.TGG
yap = EeIndexStation.YAP


dip = [bcl, cdo, ceb, dav, lkw, yap]
offdip = [gsi, lgz, mnd, mut, scn, tgg]

period = Period(start=datetime(2015, 1, 1), end=datetime(2023, 12, 31))


write_singular_eej_to_csv(
    period,
    dip_stations=dip,
    offdip_stations=offdip,
    path="data/southeast_asia_singular_eej.csv",
)
