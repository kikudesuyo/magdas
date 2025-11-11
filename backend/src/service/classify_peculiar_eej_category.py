from datetime import datetime, timedelta
from enum import Enum

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from pydantic import BaseModel
from src.plot.config import get_font_prop
from src.repository.peculiar_eej import PeculiarEejRepository
from src.service.moon_phase import get_lunar_age

# 日本語フォント（例: IPAexGothic）を指定して警告を消す
matplotlib.rcParams["font.family"] = get_font_prop().get_name()
from scipy.signal import find_peaks
from src.constants.time_relation import TimeUnit
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParam
from src.service.calc_eej_detection import BestEuelSelectorForEej, EuelData
from src.service.ee_index.factory_ee import EeFactory
from src.service.moving_avg import calc_moving_avg


class PeculiarEej(BaseModel):
    dip_euel: EuelData
    offdip_euel: EuelData


class PeculiarEejType(str, Enum):
    UNDEVELOPED = "未発達型"
    SUDDEN = "突発型"
    ERROR = "エラー"


def classify_peculiar_eej_type(times, dip_euel, offdip_euel) -> PeculiarEejType:
    # 細かい変動を捉えるために、スムージングしていないデータを使う
    dip_euel = np.array(dip_euel, dtype=float)
    offdip_euel = np.array(offdip_euel, dtype=float)
    times = np.array(times)

    hours = np.array([t.hour for t in times])
    mask_noon = (hours >= 9) & (hours < 15)

    if not mask_noon.any():
        return PeculiarEejType.ERROR

    dip_noon = dip_euel[mask_noon]
    off_noon = offdip_euel[mask_noon]

    corr = pd.Series(dip_noon).corr(pd.Series(off_noon))  # nanを無視して相関を計算

    # x: 時間やサンプル番号など、y: 観測値
    x = np.arange(len(dip_noon))

    if corr > 0.6:
        return PeculiarEejType.UNDEVELOPED

    return PeculiarEejType.SUDDEN


# csvファイルに挿入するデータを取得するのはservice層
# CSVファイルに保存するクラス←service層
# CSVファイルを読み込み、取得するクラスを作りたい←repository層


# 特異型EEJを判定する流れ。すべての日程から特異型EEJを抜き出す。抜き出した日程に対して、特異型EEJのタイプを判定する


class ClassificationPeculiarEej:
    def __init__(self):

        anc = EeIndexStation.ANC
        hua = EeIndexStation.HUA
        eus = EeIndexStation.EUS

        dip_stations = [anc, hua]
        offdip_stations = [eus]

        peculiar_eej_data = PeculiarEejRepository().select_all()

        undev_dates = []
        sudden_dates = []
        for data in peculiar_eej_data:
            start_dt = datetime.combine(data.date, datetime.min.time())
            end_dt = start_dt + timedelta(days=1) - timedelta(minutes=1)
            lt_period = Period(start=start_dt, end=end_dt)

            dip_best_euel = BestEuelSelectorForEej(
                dip_stations, lt_period.start, True
            ).select_euel_data()

            offdip_best_euel = BestEuelSelectorForEej(
                offdip_stations, lt_period.start, False
            ).select_euel_data()

            # dip_best_euel.station
            factory = EeFactory()
            dip_ut_param = StationParam(dip_best_euel.station, lt_period).to_ut_params()
            dip_euel = factory.create_euel(dip_ut_param).calc_euel()
            dip_smoothed_euel = calc_moving_avg(
                dip_euel, TimeUnit.ONE_HOUR.min, TimeUnit.THIRTY_MINUTES.min
            )

            offdip_ut_param = StationParam(
                offdip_best_euel.station, lt_period
            ).to_ut_params()
            offdip_euel = factory.create_euel(offdip_ut_param).calc_euel()
            offdip_smoothed_euel = calc_moving_avg(
                offdip_euel, TimeUnit.ONE_HOUR.min, TimeUnit.THIRTY_MINUTES.min
            )

            peculiar_eej_type = classify_peculiar_eej_type(
                times=[lt_period.start + timedelta(minutes=i) for i in range(1440)],
                dip_euel=dip_euel,
                offdip_euel=offdip_euel,
            )

            if peculiar_eej_type == PeculiarEejType.UNDEVELOPED:
                undev_dates.append(data.date)
            if peculiar_eej_type == PeculiarEejType.SUDDEN:
                sudden_dates.append(data.date)

        # Save results to DataFrame and export as CSV (English column names)
        results = []
        for date in undev_dates:
            results.append(
                {
                    "Date": date,
                    "Station": "south_america",
                    "Type": PeculiarEejType.UNDEVELOPED.value,
                }
            )
        for date in sudden_dates:
            results.append(
                {
                    "Date": date,
                    "Station": "south_america",
                    "Type": PeculiarEejType.SUDDEN.value,
                }
            )
        df = pd.DataFrame(results)
        df.to_csv("peculiar_eej_classification.csv", index=False, encoding="utf-8-sig")

    # def get_undev_dates(self) -> list[datetime]:
    #     return self.undev_dates

    # def get_sudden_dates(self) -> list[datetime]:
    #     return self.sudden_dates


ClassificationPeculiarEej()
