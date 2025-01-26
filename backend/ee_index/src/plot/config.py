from matplotlib import pyplot as plt


class PlotConfig:
    @staticmethod
    def rcparams():
        plt.rcParams["font.family"] = "Times New Roman"
        plt.rcParams["xtick.direction"] = "in"  # x軸の目盛りの向き
        plt.rcParams["ytick.direction"] = "in"  # y軸の目盛りの向き
        plt.rcParams["xtick.labelsize"] = 11  # x軸目盛りのフォントサイズ
        plt.rcParams["ytick.labelsize"] = 11  # y軸目盛りのフォントサイズ
        plt.rcParams["xtick.top"] = True  # x軸の上部目盛り
        plt.rcParams["ytick.right"] = True  # y軸の右部目盛り
        plt.rcParams["legend.fancybox"] = False  # 丸角OFF
        plt.rcParams["legend.framealpha"] = 1  # 透明度の指定、0で塗りつぶしなし
        plt.rcParams["legend.edgecolor"] = "black"  # edgeの色を変更
        plt.rcParams["legend.fontsize"] = 11  # 凡例のフォントサイズを設定
        plt.rcParams["xtick.minor.visible"] = True  # x軸補助目盛りの追加
        plt.rcParams["ytick.minor.visible"] = True  # y軸補助目盛りの追加
