from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from src.dev.plot.config import PlotConfig
from src.domain.station_params import Period
from src.service.ee_index.ee_from_kato import EeFromKatoService
from src.service.peculiar_eej import PeculiarEejService


class KatoEuelPlotter:
    def __init__(self, ut_period: Period):
        self.ut_period = ut_period
        PlotConfig.rcparams()
        self.fig, self.ax = plt.subplots(figsize=(15, 8))
        self._set_axis_labels()
        self.fig.canvas.mpl_connect("motion_notify_event", self._on_move)

    def plot_euel(self, station_code: str, color: str):
        service = EeFromKatoService(station_code)
        data = service.get_ee_data_by_range(self.ut_period)
        if not data:
            print(f"No data for {station_code} in the given period.")
            return

        full_range = pd.date_range(
            start=self.ut_period.start, end=self.ut_period.end, freq="min"
        )
        euel_series = pd.Series(index=full_range, dtype=np.float64)

        for item in data:
            euel_series[item.dt] = item.euel_data

        euel_values = euel_series.values
        x_axis = np.arange(len(euel_values))

        self.ax.plot(
            x_axis,
            euel_values,
            label=f"{station_code}_EUEL",
            color=color,
            linewidth=0.8,
        )

    def _set_axis_labels(self):
        data_length = self.ut_period.total_minutes() + 1
        self.ax.set_ylabel("EUEL (nT)", rotation=90, fontsize=12)
        self.ax.set_xlim(0, data_length)
        self.ax.set_ylim(-150, 150)
        self.ax.set_xlabel("UT", fontsize=15)

        tick_interval = max(1, data_length // 10)  # More ticks
        ticks = range(0, data_length, tick_interval)
        time_labels = [
            (self.ut_period.start + timedelta(minutes=i)).strftime("%m/%d %H:%M")
            for i in ticks
        ]
        self.ax.set_xticks(ticks)
        self.ax.set_xticklabels(time_labels, rotation=45, ha="right")  # Rotate labels
        self.fig.tight_layout()  # Adjust layout

    def _on_move(self, event):
        if not event.inaxes:
            return
        x, y = event.xdata, event.ydata
        if x is None or y is None:
            return
        minute_offset = int(x)
        current_time = self.ut_period.start + timedelta(minutes=minute_offset)
        time_str = current_time.strftime("%Y/%m/%d %H:%M")
        # Use a text box for the info to avoid title override
        if not hasattr(self, "info_text"):
            self.info_text = self.ax.text(0.01, 1.01, "", transform=self.ax.transAxes)
        self.info_text.set_text(f"Date: {time_str}, Value: {y:.2f} nT")
        self.ax.figure.canvas.draw()

    def set_title(self, title):
        self.ax.set_title(title, fontsize=15, fontweight="semibold", pad=20)

    def show(self):
        self.ax.legend(loc="upper left", fontsize=12)
        plt.grid(True, which="both", linestyle="--")
        plt.show()
        plt.close(self.fig)

    def save(self, filepath: str):
        self.ax.legend(loc="lower left", fontsize=18)
        plt.draw()
        plt.savefig(filepath)
        # self.fig.savefig(filepath, dpi=300)


if __name__ == "__main__":
    # Plot for a shorter period to see details, e.g., one month
    from src.domain.region import Region
    from src.utils.path import generate_parent_abs_path

    p = PeculiarEejService()
    peculiar_eej_data = p.get_by_region(Region.SOUTH_AMERICA)
    # dates = p.get_all()

    for d in peculiar_eej_data:
        ut_period = Period(
            start=datetime(d.date.year, d.date.month, d.date.day, 0, 0),
            end=datetime(d.date.year, d.date.month, d.date.day, 23, 59),
        )

        plotter = KatoEuelPlotter(ut_period)
        plotter.plot_euel("TTB", "blue")
        plotter.plot_euel("KOU", "green")
        plotter.plot_euel("EUS", "red")
        plotter.set_title("EUEL from Kato's data (March 2016)")

        img_path = generate_parent_abs_path(
            f"/img/peculiar_eej/brazil_region_by_kato/{d.date.strftime('%Y%m%d')}.png"
        )
        plotter.save(img_path)
