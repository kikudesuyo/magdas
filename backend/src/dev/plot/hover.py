from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable, Optional

from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseEvent
from matplotlib.figure import Figure


class HoverConfigurator:
    """
    Plot 側で用いるためのラッパークラス
    """

    def __init__(self, fig: Figure, ax: Axes, period):
        # カーソル変換ロジック
        x_conv = lambda x: period.start + timedelta(minutes=int(x))
        y_conv = float

        cursor = CursorConverter(x_conv, y_conv)
        hover_text = HoverText(fig, ax, cursor)

        # Matplotlibにイベント登録
        fig.canvas.mpl_connect("motion_notify_event", hover_text.on_hover)


@dataclass(frozen=True)
class CursorData:
    dt: datetime
    value: float


class CursorConverter:
    """
    Matplotlib のカーソルイベント(xdata, ydata)を
    ドメインデータ(CursorData)に変換する責務を持つ。
    """

    def __init__(
        self,
        x_converter: Callable[[float], datetime],
        y_converter: Callable[[float], float],
    ):
        self.x_converter = x_converter
        self.y_converter = y_converter

    def convert(self, event: MouseEvent) -> Optional[CursorData]:
        """イベントから CursorData を生成する。無効なイベントは None。"""
        if event.inaxes is None or event.xdata is None or event.ydata is None:
            return None
        return CursorData(
            dt=self.x_converter(event.xdata),
            value=self.y_converter(event.ydata),
        )


class HoverText:
    INFO_TEXT_X = 0.01
    INFO_TEXT_Y = 0.98
    LABEL_FONT_SIZE = 12
    DATE_FORMAT = "%Y/%m/%d %H:%M"
    TEXT_TEMPLATE = "Date: {ts} | Value: {value:.2f} nT"

    def __init__(self, fig: Figure, ax: Axes, cursor_converter: CursorConverter):
        self.fig = fig
        self.ax = ax
        self._cursor_converter = cursor_converter

        self._info_text = self.ax.text(
            self.INFO_TEXT_X,
            self.INFO_TEXT_Y,
            "",
            transform=self.ax.transAxes,
            va="top",
            fontsize=self.LABEL_FONT_SIZE,
        )

    def on_hover(self, event) -> None:
        """ホバーイベント時に呼び出され、情報を更新する."""
        cursor = self._cursor_converter.convert(event)
        if cursor is not None:
            self._update_info(cursor)

    def _update_info(self, cursor: CursorData) -> None:
        ts = cursor.dt.strftime(self.DATE_FORMAT)
        text = self.TEXT_TEMPLATE.format(ts=ts, value=cursor.value)
        self._info_text.set_text(text)
        self.fig.canvas.draw_idle()
