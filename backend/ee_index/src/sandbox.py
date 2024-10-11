from datetime import datetime

from ee_index.src.path import generate_abs_path
from ee_index.src.plot.daily_ee_index_plotter import DailyEeIndexPlotter

instance = DailyEeIndexPlotter(datetime(2014, 7, 3))
instance.save_ee_figure("ANC", generate_abs_path("/img/test.png"))

print(generate_abs_path("/img/test.png"))
