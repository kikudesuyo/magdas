from datetime import datetime

from ee_index.src.path import generate_abs_path
from ee_index.src.plot.daily_ee_index_plotter import DailyEeIndexPlotter

instance = DailyEeIndexPlotter(datetime(2014, 6, 3))
instance.plot_ee_figure("ANC", generate_abs_path("/img/test.png"))
