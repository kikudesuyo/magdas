from dataclasses import dataclass
from datetime import timedelta

from matplotlib.axes import Axes
from src.domain.station_params import Period


@dataclass(frozen=True)
class AxisConfig:
    y_label: str = "nT"
    y_min: int = -100
    y_max: int = 200
    x_label: str = "UT"
    xtick_divisions: int = 8  # x軸を何分割するか


class AxisConfigurator:
    def __init__(self, ax: Axes, ut_period: Period, config: AxisConfig = AxisConfig()):
        self.ax = ax
        self.ut_period = ut_period
        self.config = config

    def apply(self) -> None:
        """外部から呼ぶメインメソッド。軸の設定をまとめて適用"""
        self._set_y_axis()
        self._set_x_axis_with_time_labels()

    def _set_y_axis(self) -> None:
        self.ax.set_ylabel(self.config.y_label, rotation=0)
        self.ax.set_ylim(self.config.y_min, self.config.y_max)

    def _set_x_axis_with_time_labels(self) -> None:
        data_length = self.ut_period.total_minutes() + 1
        self.ax.set_xlim(0, data_length)
        self.ax.set_xlabel(self.config.x_label)

        tick_interval = max(1, data_length // self.config.xtick_divisions)
        ticks = range(0, data_length, tick_interval)

        time_labels = []
        prev_date = None

        for i in ticks:
            current_dt = self.ut_period.start + timedelta(minutes=i)
            current_date = current_dt.date()

            # 最初のラベル or 日付が変わった場合は「日付 + 時間」
            if prev_date is None or current_date != prev_date:
                label = current_dt.strftime("%m/%d %H:%M")
            else:
                # 同じ日なら時間だけ
                label = current_dt.strftime("%H:%M")

            prev_date = current_date
            time_labels.append(label)

        self.ax.set_xticks(ticks)
        self.ax.set_xticklabels(time_labels)
