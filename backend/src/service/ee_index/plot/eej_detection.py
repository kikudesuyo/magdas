from datetime import datetime, timedelta

import numpy as np
from matplotlib import pyplot as plt
from src.service.ee_index.calc.euel_index import get_local_euel
from src.service.ee_index.calc.moving_ave import calc_moving_ave
from src.service.ee_index.constant.magdas_station import EeIndexStation
from src.service.ee_index.constant.time_relation import Sec
from src.service.ee_index.plot.config import PlotConfig


class EejDetectionPlotter:
    def __init__(self, local_start_dt: datetime, local_end_dt: datetime):
        self.local_start_dt = local_start_dt
        self.local_end_dt = local_end_dt
        PlotConfig.rcparams()
        self.fig, self.ax = plt.subplots()
        self._set_axis_labels()
        self.fig.canvas.mpl_connect("motion_notify_event", self._on_move)

    def plot_local_euel(self, station: EeIndexStation):
        """_summary_
        TODO: 正しいデータ範囲を取り出すことが出来ていない。ERが開始時刻からN日のデータを取ってくるメソッドのせいで、期待しているデータの数と異なってしまっている。
        ERのメソッドを開始時刻と終了時刻で指定させる
        """
        local_euel = get_local_euel(station, self.local_start_dt, self.local_end_dt)
        moving_avg = calc_moving_ave(local_euel, 120, 60)
        x_axis = np.arange(0, len(moving_avg), 1)
        self.ax.plot(x_axis, moving_avg, label=station.name)

    def _set_axis_labels(self):
        data_length = (
            int((self.local_end_dt - self.local_start_dt).total_seconds())
            // Sec.ONE_MINUTE.const
            + 1
        )
        self.ax.set_ylabel("nT", rotation=0)
        self.ax.set_xlim(0, data_length)
        self.ax.set_ylim(-100, 200)
        self.ax.set_xlabel("Local Time", fontsize=15)
        tick_interval = max(1, data_length // 8)
        ticks = range(0, data_length, tick_interval)
        time_labels = [
            (self.local_start_dt + timedelta(minutes=i)).strftime("%m/%d %H:%M")
            for i in ticks
        ]
        self.ax.set_xticks(ticks)
        self.ax.set_xticklabels(time_labels)

    def _on_move(self, event):
        if not event.inaxes:
            return
        x, y = event.xdata, event.ydata
        time_str = (self.local_start_dt + timedelta(minutes=int(x))).strftime(
            "%m/%d %H:%M"
        )
        self.ax.set_title(f"Time: {time_str}, Value: {y:.2f}")
        self.ax.figure.canvas.draw()

    def show(self):
        self.ax.legend(loc="lower left", fontsize=18)
        plt.show()

    def save(self, path):
        self.ax.legend(loc="lower left", fontsize=18)
        plt.savefig(path)


start_local_dt = datetime(2014, 1, 1, 0, 0)
end_local_dt = datetime(2014, 1, 31, 23, 59)
detection = EejDetectionPlotter(start_local_dt, end_local_dt)
detection.plot_local_euel(EeIndexStation.ANC)
detection.plot_local_euel(EeIndexStation.EUS)
detection.show()
