from matplotlib import font_manager
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from src.utils.path import generate_abs_path


class PlotConfigurator:
    def __init__(self, fig: Figure, ax: Axes):
        self.fig = fig
        self.ax = ax
        self.font_prop = FontLoader().font_prop

    def apply(self):
        # font設定
        self.fig.text(0.01, 0.01, "", fontproperties=self.font_prop)
        # tick設定
        self.ax.tick_params(
            axis="x", direction="in", labelsize=11, top=True, which="both"
        )
        self.ax.tick_params(
            axis="y", direction="in", labelsize=11, right=True, which="both"
        )
        # グリッド（局所設定）
        self.ax.grid(linestyle="--", color="gray", alpha=0.7, linewidth=0.7)


class FontLoader:
    FONT_PATH = "/dev/plot/NotoSansJP-Regular.ttf"

    def __init__(self):
        font_path = generate_abs_path(self.FONT_PATH)
        font_manager.fontManager.addfont(font_path)
        self.font_prop = font_manager.FontProperties(fname=font_path)  # type: ignore (OSによって型が異なるため)
