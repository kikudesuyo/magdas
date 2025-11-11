from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Dict, List, Literal

import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict
from src.constants.ee_index import EEJ_THRESHOLD
from src.constants.time_relation import TimeUnit
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParam
from src.service.ee_index.factory_ee import EeFactory
from src.service.kp import Kp
from src.service.linear_completion import interpolate_nan
from src.service.moving_avg import calc_moving_avg


class DaytimeInterval:
    START = time(9, 0)
    END = time(14, 59)

    @classmethod
    def contains(cls, t: time) -> bool:
        return cls.START <= t <= cls.END


@dataclass
class NanRatioData:
    array: np.ndarray
    nan_ratio: float


class EuelData(BaseModel):
    # TODO Regionを定義してgm_lonでバリデーションできるようにする
    station: EeIndexStation
    array: np.ndarray

    # numpyを使うためにConfigDictを設定
    model_config = ConfigDict(arbitrary_types_allowed=True)


class BestEuelSelectorForEej:
    def __init__(self, stations: List[EeIndexStation], local_date: date, is_dip: bool):
        self.stations = stations
        self.local_date = local_date

        self._validate_stations(stations, is_dip)

    def _validate_stations(self, stations: List[EeIndexStation], is_dip: bool):
        if is_dip:
            for station in stations:
                if not station.is_dip():
                    raise ValueError(
                        f"{station.code} is {station.gm_lat}. It is not in dip region"
                    )
        else:
            for station in stations:
                if not station.is_offdip():
                    raise ValueError(
                        f"{station.code} is {station.gm_lat}. It is not in off-dip region"
                    )

    def select_euel_data(self) -> EuelData:
        eej_euels: Dict[EeIndexStation, NanRatioData] = {}
        for station in self.stations:
            eej_euel = self._euel_for_eej_detection(station)
            nan_ratio = np.sum(np.isnan(eej_euel)) / len(eej_euel)
            eej_euels[station] = NanRatioData(
                eej_euel,
                nan_ratio,
            )

        best_station, best_euel = min(eej_euels.items(), key=lambda x: x[1].nan_ratio)
        return EuelData(
            station=best_station,
            array=best_euel.array,
        )

    def _euel_for_eej_detection(self, station: EeIndexStation):
        s_lt = datetime(
            self.local_date.year, self.local_date.month, self.local_date.day, 0, 0
        )
        e_lt = s_lt.replace(hour=23, minute=59)
        lt_params = StationParam(station, Period(s_lt, e_lt))
        ut_params = lt_params.to_ut_params()

        factory = EeFactory()
        euel = factory.create_euel(ut_params)
        euel_values = euel.calc_euel()

        if not self._has_night_data(euel_values):
            return euel_values
        return self._euel_for_eej(euel_values)

    def _has_night_data(self, daily_data: np.ndarray) -> bool:
        """一日の夜間（19:00～05:00データが存在するかどうかを判定する"""
        if len(daily_data) != TimeUnit.ONE_DAY.min:
            raise ValueError("daily_data must have 1440 elements.")
        dawn_e = daily_data[0 : TimeUnit.FIVE_HOURS.min]
        dusk_e = daily_data[TimeUnit.NINETEEN_HOURS.min : TimeUnit.ONE_DAY.min]
        return not (np.all(np.isnan(dawn_e)) and np.all(np.isnan(dusk_e)))

    def _euel_for_eej(self, daily_euel_values: np.ndarray) -> np.ndarray:
        """
        夜間（19:00～05:00）をNaNで埋めて補間
        EUELから補間したベースラインを引く
        1時間の移動平均を計算
        """
        if len(daily_euel_values) != TimeUnit.ONE_DAY.min:
            raise ValueError("daily_euel_values must have 1440 elements.")
        euel_for_baseline = np.concatenate(
            (
                daily_euel_values[: TimeUnit.FIVE_HOURS.min],
                np.nan * np.ones(TimeUnit.FOURTEEN_HOURS.min),
                daily_euel_values[TimeUnit.NINETEEN_HOURS.min : TimeUnit.ONE_DAY.min],
            )
        )
        baseline = interpolate_nan(euel_for_baseline)
        euel_for_eej_detection = daily_euel_values - baseline

        return calc_moving_avg(
            euel_for_eej_detection,
            window=TimeUnit.ONE_HOUR.min,
            nan_threshold=TimeUnit.THIRTY_MINUTES.min,
        )


class EejCategory(BaseModel):
    label: Literal[
        "peculiar",  # 特異型EEJ: peculiar
        "normal",  # 通常型EEJ: normal
        "disturbance",  # 擾乱(Kp指数とEDstで判断): disturbance
        "missing",  # データ欠測: missing
    ]

    @classmethod
    def from_conditions(
        cls,
        peak_diff: float,
        daily_max_kp: float,
        daily_min_edst: float,
    ) -> "EejCategory":
        if daily_max_kp >= 4 or daily_min_edst < -30:
            return cls(label="disturbance")
        if np.isnan(peak_diff):
            return cls(label="missing")
        if peak_diff >= EEJ_THRESHOLD:
            return cls(label="normal")
        return cls(label="peculiar")


class DisturbanceCategory(BaseModel):
    label: Literal[
        "disturbance",  # 擾乱
        "quiet",  # 静穏
        "missing",  # データ欠測
    ]

    @classmethod
    def from_conditions(
        cls,
        daily_max_kp: float,
        daily_min_edst: float,
    ) -> "DisturbanceCategory":
        if np.isnan(daily_max_kp) or np.isnan(daily_min_edst):
            return cls(label="missing")
        if daily_max_kp >= 4 or daily_min_edst < -30:
            return cls(label="disturbance")
        return cls(label="quiet")


def calc_euel_peak_diff(
    dip_euel: EuelData, offdip_euel: EuelData, local_date: date
) -> float:
    timestamp = np.array(
        [
            datetime(local_date.year, local_date.month, local_date.day, 0, 0)
            + timedelta(minutes=i)
            for i in range(TimeUnit.ONE_DAY.min)
        ]
    )
    is_noon = np.array([DaytimeInterval.contains(dt.time()) for dt in timestamp])
    dip_max = np.max(dip_euel.array[is_noon])
    offdip_max = np.max(offdip_euel.array[is_noon])
    return float(dip_max - offdip_max)


class EejDetection:
    def __init__(self, peak_diff: float, local_date: date):
        self.local_date = local_date
        self.eej_peak_diff = peak_diff

    def _get_timestamp(self) -> NDArray[np.datetime64]:
        start_lt = datetime(
            self.local_date.year, self.local_date.month, self.local_date.day, 0, 0
        )
        return np.array(
            [start_lt + timedelta(minutes=i) for i in range(TimeUnit.ONE_DAY.min)]
        )

    def _calc_daily_min_edst(self):
        s_dt = datetime(
            self.local_date.year, self.local_date.month, self.local_date.day, 0, 0
        )
        e_dt = s_dt.replace(hour=23, minute=59)
        period = Period(s_dt, e_dt)
        factory = EeFactory()
        edst = factory.create_edst(period)
        return np.min(edst.calc_edst())

    def _get_daily_max_kp(self):
        s_dt = datetime(
            self.local_date.year, self.local_date.month, self.local_date.day, 0, 0
        )
        e_dt = s_dt.replace(hour=23, minute=59)
        kp = Kp().get_max_of_day(s_dt, e_dt)
        return kp

    def is_eej_peak_diff_nan(self):
        """データ欠損か判定"""
        return np.isnan(self.eej_peak_diff)

    def is_eej_present(self):
        return self.eej_peak_diff >= EEJ_THRESHOLD

    def is_peculiar_eej(self):
        return self.classify_eej_category().label == "peculiar"

    def classify_eej_category(self) -> EejCategory:
        daily_max_kp = self._get_daily_max_kp()
        daily_min_edst = self._calc_daily_min_edst()
        return EejCategory.from_conditions(
            peak_diff=self.eej_peak_diff,
            daily_max_kp=daily_max_kp,
            daily_min_edst=daily_min_edst,
        )
