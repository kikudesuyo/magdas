from datetime import datetime

from src.dev.save_singular_eej import write_singular_eej_to_csv
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period
from src.plot.plot_ee_index import EeIndexPlotter
from src.plot.plot_eej_detection import EejDetectionPlotter

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


dips = [bcl, cdo, ceb, dav, lkw, yap]
offdips = [gsi, lgz, mnd, mut, scn, tgg]

period = Period(start=datetime(2015, 1, 1), end=datetime(2022, 12, 31))


"""dip, offDipのEUELの値を確認する"""

# dip_ee_plotter = EeIndexPlotter(period)
# dip_ee_plotter.plot_euel(bcl, color="red")
# dip_ee_plotter.plot_euel(cdo, color="orange")
# dip_ee_plotter.plot_euel(ceb, color="yellow")
# dip_ee_plotter.plot_euel(dav, color="green")
# dip_ee_plotter.plot_euel(lkw, color="blue")
# dip_ee_plotter.plot_euel(yap, color="purple")
# dip_ee_plotter.set_title("Dip Stations EUEL")
# dip_ee_plotter.show()

# offdip_ee_plotter = EeIndexPlotter(period)
# offdip_ee_plotter.plot_euel(gsi, color="red")
# offdip_ee_plotter.plot_euel(lgz, color="orange")
# offdip_ee_plotter.plot_euel(mnd, color="yellow")
# offdip_ee_plotter.plot_euel(mut, color="green")
# offdip_ee_plotter.plot_euel(scn, color="blue")
# offdip_ee_plotter.plot_euel(tgg, color="purple")
# offdip_ee_plotter.set_title("OffDip Stations EUEL")
# offdip_ee_plotter.show()


write_singular_eej_to_csv(
    period,
    dip_stations=dips,
    offdip_stations=offdips,
    path="data/southeast_asia_singular_eej.csv",
)
