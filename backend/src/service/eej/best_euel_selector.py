from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime
from typing import List, final

import numpy as np
from src.constants.time_relation import TimeUnit
from src.domain.magdas_station import EeIndexStation
from src.domain.region import Region
from src.domain.station_params import Period, StationParam
from src.model.euel_data import EuelData
from src.service.calc_utils.linear_completion import interpolate_nan
from src.service.calc_utils.moving_avg import calc_moving_avg
from src.service.ee_index.intermag_ee import IntermagEuelService
from src.service.ee_index.magdas_ee import MagdasEeService, MagdasEuelService


@dataclass
class NanRatioData:
    array: np.ndarray
    nan_ratio: float


class BaseEuelSelectorForEej(ABC):
    def __init__(
        self,
        region: Region,
        stations: List[EeIndexStation],
        local_date: date,
        is_dip: bool,
    ):
        self._validate_stations(stations, is_dip)
        self.region = region
        self.stations = stations
        self.local_date = local_date

    @abstractmethod
    def load_daily_euel(self, station: EeIndexStation) -> EuelData:
        """データソース（Magdas or Intermag）から1日のEUELを読み込む。"""
        ...

    @final
    def select_best_euel_data(self) -> EuelData:
        eej_euels = {}

        for station in self.stations:
            daily_euel = self.load_daily_euel(station)
            processed_euel = self._euel_for_eej(daily_euel)
            nan_ratio = np.sum(np.isnan(processed_euel)) / len(processed_euel)

            eej_euels[station] = NanRatioData(
                array=processed_euel,
                nan_ratio=nan_ratio,
            )

        best_station, best = min(eej_euels.items(), key=lambda x: x[1].nan_ratio)

        return EuelData(
            region=self.region,
            station=best_station,
            array=best.array,
        )

    def _euel_for_eej_detection(self, station: EeIndexStation) -> EuelData:
        s_lt = datetime(
            self.local_date.year, self.local_date.month, self.local_date.day, 0, 0
        )
        e_lt = s_lt.replace(hour=23, minute=59)
        lt_params = StationParam(station, Period(s_lt, e_lt))
        ut_params = lt_params.to_ut_params()

        ee_service = MagdasEeService(ut_params)
        ee_data = ee_service.calc_all()

        euel_data = EuelData(region=self.region, station=station, array=ee_data.euel)
        if self._has_night_data(euel_data):
            return EuelData(
                region=self.region,
                station=station,
                array=self._euel_for_eej(  # 夜間データ補間＋ベースライン引き＋1時間移動平均
                    EuelData(region=self.region, station=station, array=ee_data.euel)
                ),
            )
        return euel_data

    def _has_night_data(self, daily_data: EuelData) -> bool:
        """一日の夜間（19:00～05:00データが存在するかどうかを判定する"""
        daily_euel_values = daily_data.array
        if len(daily_euel_values) != TimeUnit.ONE_DAY.min:
            raise ValueError("daily_data must have 1440 elements.")
        dawn_e = daily_euel_values[0 : TimeUnit.FIVE_HOURS.min]
        dusk_e = daily_euel_values[TimeUnit.NINETEEN_HOURS.min : TimeUnit.ONE_DAY.min]
        return not (np.all(np.isnan(dawn_e)) and np.all(np.isnan(dusk_e)))

    def _euel_for_eej(self, daily_euel: EuelData) -> np.ndarray:
        """
        夜間（19:00～05:00）をNaNで埋めて補間
        EUELから補間したベースラインを引く
        1時間の移動平均を計算
        """
        daily_euel_values = daily_euel.array
        if len(daily_euel_values) != TimeUnit.ONE_DAY.min:
            raise ValueError("daily_euel_values must have 1440 elements.")
        if np.all(np.isnan(daily_euel_values)):
            return daily_euel_values

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

    def _validate_stations(self, stations, is_dip):
        if is_dip:
            for s in stations:
                if not s.is_dip():
                    raise ValueError(f"{s.code} is not dip-region")
        else:
            for s in stations:
                if not s.is_offdip():
                    raise ValueError(f"{s.code} is not off-dip region")


class MagdasEuelSelectorForEej(BaseEuelSelectorForEej):
    """EEJ検知する上で、一番良いデータを持つ観測点を判定しそのEUELデータを返すクラス"""

    def load_daily_euel(self, station: EeIndexStation) -> EuelData:
        s_lt = datetime(
            self.local_date.year, self.local_date.month, self.local_date.day, 0, 0
        )
        e_lt = s_lt.replace(hour=23, minute=59)
        lt_params = StationParam(station, Period(s_lt, e_lt))
        ut_params = lt_params.to_ut_params()

        ee_service = MagdasEuelService(ut_params)
        euel_array = ee_service.calc()
        return EuelData(
            region=self.region,
            station=station,
            array=euel_array,
        )


class IntermagEuelSelectorForEej(BaseEuelSelectorForEej):
    """
    EEJ検知する上で、一番良いデータを持つ観測点を判定しそのEUELデータを返すクラス
    現状はブラジル地域のみ対応
    """

    def load_daily_euel(self, station: EeIndexStation) -> EuelData:
        s_lt = datetime(
            self.local_date.year, self.local_date.month, self.local_date.day, 0, 0
        )
        e_lt = s_lt.replace(hour=23, minute=59)
        lt_params = StationParam(station, Period(s_lt, e_lt))
        ut_params = lt_params.to_ut_params()

        ee_service = IntermagEuelService(ut_params, Region.BRAZIL)
        return ee_service.get_euel_data_by_range()


class BestEuelSelectorFactory:
    def create(
        self,
        region: Region,
        stations: List[EeIndexStation],
        local_date: date,
        is_dip: bool,
    ) -> BaseEuelSelectorForEej:
        if region == Region.SOUTH_AMERICA:
            return MagdasEuelSelectorForEej(region, stations, local_date, is_dip)
        if region == Region.BRAZIL:
            return IntermagEuelSelectorForEej(region, stations, local_date, is_dip)
        raise ValueError(f"Unsupported region: {region}")
