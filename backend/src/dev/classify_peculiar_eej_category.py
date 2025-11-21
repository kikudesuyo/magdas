from datetime import datetime, timedelta
from enum import Enum
from typing import List

import numpy as np
import pandas as pd
from src.domain.magdas_station import EeIndexStation
from src.domain.region import Region
from src.domain.station_params import Period
from src.model.peculiar_eej import PeculiarEejModel
from src.service.calc_eej_detection import (
    BestEuelSelectorForEej,
    EejDetection,
    EuelData,
    calc_euel_peak_diff,
)
from src.service.peculiar_eej import PeculiarEejService


class PeculiarEejType(str, Enum):
    UNDEVELOPED = "未発達型"
    SUDDEN = "突発型"
    ERROR = "エラー"


def classify_peculiar_eej_type(
    times, dip_euel_data: EuelData, offdip_euel_data: EuelData
) -> PeculiarEejType:
    # 細かい変動を捉えるために、スムージングしていないデータを使う
    dip_euel_val = np.array(dip_euel_data.array, dtype=float)
    offdip_euel_val = np.array(offdip_euel_data.array, dtype=float)
    times = np.array(times)

    hours = np.array([t.hour for t in times])
    mask_noon = (hours >= 9) & (hours < 15)

    if not mask_noon.any():
        return PeculiarEejType.ERROR

    dip_noon = dip_euel_val[mask_noon]
    off_noon = offdip_euel_val[mask_noon]
    corr = pd.Series(dip_noon).corr(pd.Series(off_noon))  # nanを無視して相関を計算

    if corr > 0.6:
        return PeculiarEejType.UNDEVELOPED

    return PeculiarEejType.SUDDEN


class ClassificationPeculiarEej:
    """特異型EEJの分類を行い,CSVに保存するクラス"""

    def __init__(
        self,
        lt_period: Period,
        dip_stations: List[EeIndexStation],
        offdip_stations: List[EeIndexStation],
        region: Region,
    ):
        self.lt_period = lt_period
        self.dip_stations = dip_stations
        self.offdip_stations = offdip_stations
        self.region = region

    def aggregate_peculiar_eej_data(self) -> List[PeculiarEejModel]:
        peculiar_eej_data_list: List[PeculiarEejModel] = []
        for lt_date in (
            self.lt_period.start.date() + timedelta(days=i)
            for i in range(
                (self.lt_period.end.date() - self.lt_period.start.date()).days + 1
            )
        ):
            print(f"[Debug] Processing date: {lt_date}")
            # 使用するEUELのデータを取得
            dip_euel_selector = BestEuelSelectorForEej(
                self.region, dip_stations, lt_date, True
            )
            offdip_euel_selector = BestEuelSelectorForEej(
                self.region, offdip_stations, lt_date, False
            )
            dip_euel = dip_euel_selector.select_euel_data()
            offdip_euel = offdip_euel_selector.select_euel_data()
            peak_diff = calc_euel_peak_diff(dip_euel, offdip_euel, lt_date)
            # EEJの種類を分類
            eej_detection = EejDetection(peak_diff, lt_date)
            eej_type = eej_detection.classify_eej_category()
            if eej_type.label != "peculiar":
                continue
            # 特異型EEJの中で未発達型か突発型かを分類
            peculiar_eej_type = classify_peculiar_eej_type(
                times=[
                    datetime.combine(lt_date, datetime.min.time())
                    + timedelta(minutes=i)
                    for i in range(1440)
                ],
                dip_euel_data=dip_euel,
                offdip_euel_data=offdip_euel,
            )
            peculiar_eej_data = PeculiarEejModel(
                date=lt_date,
                region=self.region,
                type=peculiar_eej_type.value,
            )
            peculiar_eej_data_list.append(peculiar_eej_data)
        return peculiar_eej_data_list

    def save(self):
        peculiar_eej_data_list = self.aggregate_peculiar_eej_data()
        PeculiarEejService().add_peculiar_eej(peculiar_eej_data_list)


if __name__ == "__main__":
    dip_stations = [EeIndexStation.ANC, EeIndexStation.HUA]
    offdip_stations = [EeIndexStation.EUS]
    region = Region.SOUTH_AMERICA
    lt_period = Period(datetime(2008, 1, 1, 0, 0), datetime(2008, 1, 31, 23, 59))
    classification = ClassificationPeculiarEej(
        lt_period, dip_stations, offdip_stations, region=region
    )
    classification.save()
