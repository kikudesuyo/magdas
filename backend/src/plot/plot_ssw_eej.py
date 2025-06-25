from datetime import time, timedelta

from matplotlib import pyplot as plt
from matplotlib.backend_bases import MouseEvent
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period
from src.plot.plot_config import PlotConfig
from src.usecase.ssw import Ssw


class SswPlotter:
    def __init__(self, lt_period: Period):
        self.lt_period = lt_period
        PlotConfig.rcparams()
        self.fig, self.ax = plt.subplots()

    def _validate_period(self):
        if self.lt_period.start.time() != time(
            0, 0
        ) or self.lt_period.end.time() != time(23, 59):
            raise ValueError("start_lt must be 00:00 and end_lt must be 23:59.")

    def plot_ssw(self, color):
        start, end = self.lt_period.start, self.lt_period.end
        ssw_data = Ssw().get_ssw_by_range(start, end)
        self.ax.set_ylabel("K", rotation=0)
        self.ax.plot(ssw_data["Date"], ssw_data["T_90N_K"], label="SSW", color=color)
        self.fig.autofmt_xdate()
        return self.ax

    def _on_move(self, event: MouseEvent):
        if not event.inaxes:
            return
        x, y = event.xdata, event.ydata
        if x is None or y is None:
            return
        time_str = (self.lt_period.start + timedelta(minutes=int(x))).strftime(
            "%m/%d %H:%M"
        )
        self.ax.set_title(f"Time: {time_str}, Value: {y:.2f}")
        self.ax.figure.canvas.draw()

    def set_title(self, title):
        self.ax.set_title(title, fontsize=15, fontweight="semibold", pad=10)

    def show(self):
        self.ax.legend(loc="lower left", fontsize=18)
        plt.show()

    def save(self, path):
        self.ax.legend(loc="lower left", fontsize=18)
        plt.savefig(path)
        plt.close(self.fig)


if __name__ == "__main__":
    from datetime import datetime

    dip_stations = [EeIndexStation.ANC, EeIndexStation.HUA]
    offdip_stations = [EeIndexStation.EUS]

    for year in range(2015, 2024):
        start = datetime(year, 11, 1, 0, 0)
        end = datetime(year + 1, 2, 28, 23, 59)
        ut_period = Period(start, end)
        d = SswPlotter(ut_period)
        d.plot_ssw("blue")
        d.set_title(f"SSW Temperature Plot {year}")
        filename = f"img/ssw_plot_{year}.png"
        d.save(filename)
