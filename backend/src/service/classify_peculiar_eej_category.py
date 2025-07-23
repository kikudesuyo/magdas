from datetime import date, datetime, timedelta

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pydantic import BaseModel
from src.plot.config import get_font_prop

# 日本語フォント（例: IPAexGothic）を指定して警告を消す
matplotlib.rcParams["font.family"] = get_font_prop().get_name()
from scipy.signal import find_peaks
from src.constants.time_relation import TimeUnit
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.service.calc_eej_detection import BestEuelSelectorForEej, EuelData
from src.service.ee_index.factory_ee import EeFactory
from src.service.moving_avg import calc_moving_avg


def classify_euel_pattern(dip_euel, offdip_euel, time_axis=None, plot=False, title=""):
    """
    移動平均済みEUEL事象のパターンを分類する関数（シンプル版）

    Parameters:
    -----------
    dip_euel : array-like
        dip_euelの時系列データ（赤線、移動平均済み）
    offdip_euel : array-like
        offdip_euelの時系列データ（紫線、移動平均済み）
    time_axis : array-like, optional
        時間軸（プロット用）
    plot : bool
        結果をプロットするかどうか
    title : str
        プロットのタイトル

    Returns:
    --------
    str
        分類結果（"急落型", "CEJ型", "未発達型", "uncertain"）
    """

    dayside_dip_euel = dip_euel[60 * 6 : 60 * 18]  # 日中のdip_euelデータ
    dayside_offdip_euel = offdip_euel[60 * 6 : 60 * 18]  # 日中のoffdip_euelデータ

    noon_dip_euel = dip_euel[60 * 9 : 60 * 15]  # 正午のdip_euelデータ
    noon_offdip_euel = offdip_euel[60 * 9 : 60 * 15]  # 正午のoffdip_euelデータ

    # 1. 相関係数による類似度評価
    correlation = np.corrcoef(dayside_dip_euel, dayside_offdip_euel)[0, 1]

    # 2. dip_euelのピーク検出（正と負の両方）

    max_val = np.max(noon_dip_euel)
    min_val = np.min(noon_dip_euel)
    signal_range = max_val - min_val

    # 正のピーク検出
    positive_peaks = []
    if max_val > 5:
        pos_peaks, _ = find_peaks(
            dayside_dip_euel, height=max_val * 0.2, distance=len(dayside_dip_euel) // 10
        )
        positive_peaks = pos_peaks[dayside_dip_euel[pos_peaks] > max_val * 0.5]

    # 負のピーク検出（反転してピーク検出）
    negative_peaks = []
    if abs(min_val) > 5:
        neg_peaks, _ = find_peaks(
            -dayside_dip_euel,
            height=abs(min_val) * 0.2,
            distance=len(dayside_dip_euel) // 10,
        )
        negative_peaks = neg_peaks[dayside_dip_euel[neg_peaks] < min_val * 0.5]

    # 3. 全ての主要な極値（ピークと谷）
    total_peaks = len(positive_peaks) + len(negative_peaks)

    # デバッグ情報
    print(f"分析結果:")
    print(f"  相関係数: {correlation:.3f}")
    print(f"  最大値: {max_val:.1f}, 最小値: {min_val:.1f}")
    print(f"  信号範囲: {signal_range:.1f}")
    print(f"  正のピーク数: {len(positive_peaks)}, 負のピーク数: {len(negative_peaks)}")
    print(f"  総ピーク数: {total_peaks}")

    if signal_range < 10:  # 信号が小さすぎる
        result = "uncertain"
    elif correlation > 0.8:  # 高い相関がある
        result = "未発達型"
    elif total_peaks >= 2:  # 複数の主要な極値がある
        if min_val > 0:
            result = "急落型"
        else:
            result = "CEJ型"
    else:  # その他
        result = "uncertain"

    # プロット
    if plot:
        if time_axis is None:
            time_axis = np.arange(len(dayside_dip_euel))

        plt.figure(figsize=(10, 6))
        plt.plot(time_axis, dayside_dip_euel, "r-", label="HUA_FUEL", linewidth=2)
        plt.plot(
            time_axis, dayside_offdip_euel, "purple", label="EUS_FUEL", linewidth=2
        )

        plt.grid(True, alpha=0.3)
        plt.xlabel("Time")
        plt.ylabel("nT")
        plt.ylim(-100, 200)

        plt.legend()
        plt.title(f"{title} - Pattern: {result.upper()}")
        plt.tight_layout()
        plt.show()

    return result


class PeculiarEej(BaseModel):
    dip_euel: EuelData
    offdip_euel: EuelData


# テスト実行
if __name__ == "__main__":

    anc = EeIndexStation.ANC
    hua = EeIndexStation.HUA
    eus = EeIndexStation.EUS

    dip_stations = [anc, hua]
    offdip_stations = [eus]

    dates = [
        datetime(2016, 4, 5),
        datetime(2016, 11, 8),
        datetime(2017, 2, 7),
        datetime(2017, 7, 3),
        datetime(2017, 7, 30),
        datetime(2017, 8, 1),
        datetime(2017, 8, 2),
        datetime(2017, 11, 29),
        datetime(2017, 12, 10),
        datetime(2018, 2, 7),
        datetime(2018, 11, 18),
        datetime(2018, 12, 20),
        datetime(2019, 4, 24),
        datetime(2019, 6, 14),
        datetime(2019, 6, 14),
        datetime(2019, 7, 18),
        datetime(2019, 11, 5),
        datetime(2019, 11, 6),
        datetime(2019, 11, 11),
        datetime(2019, 11, 24),
        datetime(2020, 2, 15),
        datetime(2020, 2, 22),
        datetime(2020, 2, 25),
        datetime(2020, 3, 4),
        datetime(2020, 3, 5),
        datetime(2020, 3, 6),
        datetime(2020, 3, 8),
        datetime(2020, 4, 2),
        datetime(2020, 6, 12),
        datetime(2020, 6, 14),
        datetime(2020, 6, 17),
        datetime(2020, 6, 19),
        datetime(2020, 6, 27),
        datetime(2020, 7, 3),
        datetime(2020, 7, 4),
        datetime(2020, 7, 11),
        datetime(2020, 8, 15),
        datetime(2020, 8, 25),
    ]
    for d in dates:
        lt_period = Period(start=d, end=d + timedelta(days=1) - timedelta(minutes=1))

        dip_best_euel = BestEuelSelectorForEej(
            dip_stations, lt_period.start, True
        ).select_euel_data()

        offdip_best_euel = BestEuelSelectorForEej(
            offdip_stations, lt_period.start, False
        ).select_euel_data()

        # dip_best_euel.station
        factory = EeFactory()
        dip_ut_param = StationParams(dip_best_euel.station, lt_period).to_ut_params()
        dip_euel = factory.create_euel(dip_ut_param).calc_euel()
        dip_smoothed_euel = calc_moving_avg(
            dip_euel, TimeUnit.ONE_HOUR.min, TimeUnit.THIRTY_MINUTES.min
        )

        offdip_ut_param = StationParams(
            offdip_best_euel.station, lt_period
        ).to_ut_params()
        offdip_euel = factory.create_euel(offdip_ut_param).calc_euel()
        offdip_smoothed_euel = calc_moving_avg(
            offdip_euel, TimeUnit.ONE_HOUR.min, TimeUnit.THIRTY_MINUTES.min
        )

        result1 = classify_euel_pattern(
            dip_smoothed_euel,
            offdip_smoothed_euel,
            plot=True,
            title="Similar Pattern",
        )
        print(result1)
