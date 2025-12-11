"""加藤さんからいただいたデータからEUELのプロット"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from src.dev.plot.config import PlotConfig
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParam
from src.service.ee_index.intermag_ee import IntermagEuelService
from src.service.peculiar_eej import PeculiarEejService


@dataclass(frozen=True)
class CursorData:
    dt: datetime
    value: float


class CursorMapper:
    def __init__(self, period: Period):
        self._start = period.start

    def map(self, event) -> Optional[CursorData]:
        if not self._is_valid_event(event):
            return None

        return CursorData(
            dt=self._to_datetime(event.xdata),
            value=self._to_value(event.ydata),
        )

    @staticmethod
    def _is_valid_event(event) -> bool:
        return (
            event.inaxes is not None
            and event.xdata is not None
            and event.ydata is not None
        )

    def _to_datetime(self, x: float) -> datetime:
        return self._start + timedelta(minutes=int(x))

    @staticmethod
    def _to_value(y: float) -> float:
        return float(y)


class KatoEuelPlotter:
    # ===== Style 定数 =====
    FIG_SIZE = (15, 8)

    TITLE_FONT_SIZE = 15
    LABEL_FONT_SIZE = 12
    TICK_FONT_SIZE = 10

    INFO_TEXT_X = 0.01
    INFO_TEXT_Y = 0.98

    Y_LIM_MIN = -150
    Y_LIM_MAX = 150

    GRID_STYLE = "--"
    LEGEND_FONT_SIZE = 12

    def __init__(self, ut_period: Period):
        self._period = ut_period

        PlotConfig.rcparams()

        self.fig, self.ax = plt.subplots(figsize=self.FIG_SIZE)

        self._cursor_mapper = CursorMapper(self._period)

        self._init_axes()
        self._init_info_box()

        self.fig.canvas.mpl_connect("motion_notify_event", self._on_hover)

    def _init_axes(self) -> None:
        self._set_limits()
        self._set_labels()
        self._set_ticks()

    def _init_info_box(self) -> None:
        self._info_text = self.ax.text(
            self.INFO_TEXT_X,
            self.INFO_TEXT_Y,
            "",
            transform=self.ax.transAxes,
            va="top",
            fontsize=self.LABEL_FONT_SIZE,
        )

    def plot_euel(self, station: EeIndexStation, color: str) -> None:
        service = IntermagEuelService(
            StationParam(station=station, period=self._period)
        )
        data = service.get_euel_data_by_range()

        if not data:
            print(f"No data for {station.code}")
            return

        x = np.arange(len(data))
        y = np.array(data, dtype=float)

        self.ax.plot(
            x,
            y,
            label=f"{station.code}_EUEL",
            color=color,
            linewidth=0.8,
        )

    def _set_limits(self) -> None:
        length = self._period.total_minutes() + 1
        self.ax.set_xlim(0, length)
        self.ax.set_ylim(self.Y_LIM_MIN, self.Y_LIM_MAX)

    def _set_labels(self) -> None:
        self.ax.set_ylabel("EUEL (nT)", fontsize=self.LABEL_FONT_SIZE)
        self.ax.set_xlabel("UT", fontsize=self.TITLE_FONT_SIZE)

    def _set_ticks(self) -> None:
        length = self._period.total_minutes() + 1
        interval = self._calc_tick_interval(length)

        ticks = range(0, length, interval)
        labels = [
            (self._period.start + timedelta(minutes=i)).strftime("%m/%d %H:%M")
            for i in ticks
        ]

        self.ax.set_xticks(ticks)
        self.ax.set_xticklabels(
            labels, rotation=45, ha="right", fontsize=self.TICK_FONT_SIZE
        )

    @staticmethod
    def _calc_tick_interval(length: int) -> int:
        return max(1, length // 10)

    def _on_hover(self, event) -> None:
        cursor = self._cursor_mapper.map(event)
        if cursor is None:
            return

        self._update_info(cursor)

    def _update_info(self, cursor: CursorData) -> None:
        text = self._format_cursor_text(cursor)
        self._info_text.set_text(text)
        self.fig.canvas.draw_idle()

    @staticmethod
    def _format_cursor_text(cursor: CursorData) -> str:
        ts = cursor.dt.strftime("%Y/%m/%d %H:%M")
        return f"Date: {ts} | Value: {cursor.value:.2f} nT"

    def set_title(self, title: str) -> None:
        self.ax.set_title(
            title,
            fontsize=self.TITLE_FONT_SIZE,
            fontweight="semibold",
            pad=20,
        )

    def show(self) -> None:
        self._finalize()
        plt.show()
        plt.close(self.fig)

    def save(self, path: str) -> None:
        self._finalize()
        self.fig.savefig(path, dpi=300)

    def _finalize(self) -> None:
        self.ax.legend(loc="upper right", fontsize=self.LEGEND_FONT_SIZE)
        self.ax.grid(True, linestyle=self.GRID_STYLE)
        self.fig.tight_layout()


if __name__ == "__main__":
    from src.domain.region import Region
    from src.utils.path import generate_parent_abs_path

    service = PeculiarEejService()
    data_list = service.get_by_region(Region.SOUTH_AMERICA)

    for d in data_list:
        period = Period(
            start=datetime(d.date.year, d.date.month, d.date.day, 0, 0),
            end=datetime(d.date.year, d.date.month, d.date.day, 23, 59),
        )

        plotter = KatoEuelPlotter(period)

        plotter.plot_euel(EeIndexStation.TTB, "blue")
        plotter.plot_euel(EeIndexStation.KOU, "green")
        plotter.plot_euel(EeIndexStation.EUS, "red")

        plotter.set_title("Brazil Region EUEL on " + d.date.strftime("%Y/%m/%d"))

        plotter.show()

        out_path = generate_parent_abs_path(
            f"/img/peculiar_eej/brazil_region_by_kato/{d.date.strftime('%Y%m%d')}.png"
        )

        # plotter.save(out_path)
