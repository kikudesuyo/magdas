from datetime import datetime

from src.dev.save_singular_eej import write_singular_eej_to_csv
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period
from src.plot.plot_ee_index import EeIndexPlotter

anc = EeIndexStation.ANC
hua = EeIndexStation.HUA
eus = EeIndexStation.EUS


dips = [anc, hua]
offdips = [eus]

year = 2015


period = Period(start=datetime(2015, 1, 1), end=datetime(2015, 1, 31))


# write_singular_eej_to_csv(
#     period,
#     dip_stations=dips,
#     offdip_stations=offdips,
#     path="data/south_america_singular_eej.csv",
# )


ee_index_plotter = EeIndexPlotter(period)
ee_index_plotter.plot_euel(anc, color="red")
ee_index_plotter.plot_euel(hua, color="orange")
ee_index_plotter.plot_euel(eus, color="blue")
ee_index_plotter.set_title("South America EE Index")
ee_index_plotter.show()
