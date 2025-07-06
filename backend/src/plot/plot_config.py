from matplotlib import font_manager
from matplotlib import pyplot as plt
from src.utils.path import generate_parent_abs_path


class PlotConfig:
    @staticmethod
    def rcparams():
        font_prop = get_font_prop()
        plt.rcParams["font.family"] = font_prop.get_name()
        plt.rcParams["xtick.direction"] = "in"  # x軸の目盛りの向き
        plt.rcParams["ytick.direction"] = "in"  # y軸の目盛りの向き
        plt.rcParams["xtick.labelsize"] = 11  # x軸目盛りのフォントサイズ
        plt.rcParams["grid.linestyle"] = "--"  # グリッド線のスタイル
        plt.rcParams["grid.color"] = "gray"  # グリッド線の色
        plt.rcParams["grid.alpha"] = 0.7  # グリッド線の透明度
        plt.rcParams["grid.linewidth"] = 0.7  # グリッド線の幅
        plt.rcParams["axes.grid"] = True  # グリッドを表示
        plt.rcParams["ytick.labelsize"] = 11  # y軸目盛りのフォントサイズ
        plt.rcParams["xtick.top"] = True  # x軸の上部目盛り
        plt.rcParams["ytick.right"] = True  # y軸の右部目盛り
        plt.rcParams["legend.fancybox"] = False  # 丸角OFF
        plt.rcParams["legend.framealpha"] = 1  # 透明度の指定、0で塗りつぶしなし
        plt.rcParams["legend.edgecolor"] = "black"  # edgeの色を変更
        plt.rcParams["legend.fontsize"] = 11  # 凡例のフォントサイズを設定
        plt.rcParams["xtick.minor.visible"] = True  # x軸補助目盛りの追加
        plt.rcParams["ytick.minor.visible"] = True  # y軸補助目盛りの追加


def get_font_prop():
    font_path = generate_parent_abs_path("/fonts/NotoSansJP-Regular.ttf")
    font_manager.fontManager.addfont(font_path)
    return font_manager.FontProperties(fname=font_path)  # type: ignore (OSによって型が異なるため)
