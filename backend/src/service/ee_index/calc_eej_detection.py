from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Dict, List

import numpy as np
from numpy.typing import NDArray
from src.constants.ee_index import EEJ_THRESHOLD
from src.constants.time_relation import TimeUnit
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.service.ee_index.calc_linear_completion import interpolate_nan
from src.service.ee_index.calc_moving_avg import calc_moving_avg
from src.service.ee_index.factory_ee import EeFactory
from src.service.kp import Kp


class EejDetectionTime:
    START = time(9, 0)
    END = time(14, 59)

    @classmethod
    def contains(cls, t: time) -> bool:
        return cls.START <= t <= cls.END


@dataclass
class NanRatioData:
    array: np.ndarray
    nan_ratio: float


class BestEuelSelector:
    def __init__(self, stations: List[EeIndexStation], local_date: date):
        self.stations = stations
        self.local_date = local_date

    def select_euel_values(self) -> NDArray[np.float64]:
        eej_euels: Dict[EeIndexStation, NanRatioData] = {}
        for station in self.stations:
            eej_euel = self._euel_for_eej_detection(station)
            nan_count = np.sum(np.isnan(eej_euel))
            nan_ratio = nan_count / len(eej_euel)
            eej_euels[station] = NanRatioData(
                eej_euel,
                nan_ratio,
            )

        _, best_euel = min(eej_euels.items(), key=lambda x: x[1].nan_ratio)
        return best_euel.array

    def _euel_for_eej_detection(self, station: EeIndexStation):
        s_lt = datetime(
            self.local_date.year, self.local_date.month, self.local_date.day, 0, 0
        )
        e_lt = s_lt.replace(hour=23, minute=59)
        lt_params = StationParams(station, Period(s_lt, e_lt))
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


class EejDetection:
    def __init__(
        self,
        dip_stations: List[EeIndexStation],
        offdip_stations: List[EeIndexStation],
        local_date: date,
    ):
        self._validate_stations(dip_stations, offdip_stations)

        self.dip_stations = dip_stations
        self.offdip_stations = offdip_stations
        self.local_date = local_date
        self.eej_peak_diff = self.calc_eej_peak_diff()

    def _validate_stations(
        self, dip_stations: List[EeIndexStation], offdip_stations: List[EeIndexStation]
    ):
        for dip_station in dip_stations:
            if not dip_station.is_dip():
                raise ValueError(
                    f"{dip_station.code} is {dip_station.gm_lat}. It is not in dip region"
                )
        for offdip_station in offdip_stations:
            if not offdip_station.is_offdip():
                raise ValueError(
                    f"{offdip_station.code} is {offdip_station.gm_lat}. It is not in off-dip region"
                )

    def calc_eej_peak_diff(self) -> float:
        """EEJピーク差を計算。データ欠損が著しい場合はNaNを返す。"""
        best_selector = BestEuelSelector(self.dip_stations, self.local_date)
        dip_eej_euel = best_selector.select_euel_values()
        offdip_selector = BestEuelSelector(self.offdip_stations, self.local_date)
        offdip_eej_euel = offdip_selector.select_euel_values()

        timestamp = self._get_timestamp()
        is_noon = np.array([EejDetectionTime.contains(dt.time()) for dt in timestamp])
        dip_max = np.max(dip_eej_euel[is_noon])
        offdip_max = np.max(offdip_eej_euel[is_noon])
        return float(dip_max - offdip_max)

    def _get_timestamp(self) -> NDArray[np.datetime64]:
        start_lt = datetime(
            self.local_date.year, self.local_date.month, self.local_date.day, 0, 0
        )
        return np.array(
            [start_lt + timedelta(minutes=i) for i in range(TimeUnit.ONE_DAY.min)]
        )

    def _calc_min_edst(self):
        s_dt = datetime(
            self.local_date.year, self.local_date.month, self.local_date.day, 0, 0
        )
        e_dt = s_dt.replace(hour=23, minute=59)
        period = Period(s_dt, e_dt)
        factory = EeFactory()
        edst = factory.create_edst(period)
        return np.min(edst.calc_edst())

    def _get_kp(self):
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

    def is_singular_eej(self):
        kp = self._get_kp()
        if kp >= 4:
            return False
        min_edst = self._calc_min_edst()
        if min_edst < -30:
            return False
        if self.is_eej_peak_diff_nan():
            return False
        if self.is_eej_present():
            return False
        return True


if __name__ == "__main__":

    from src.utils.period import create_month_period

    anc = EeIndexStation.ANC
    hua = EeIndexStation.HUA
    eus = EeIndexStation.EUS

    year = 2015
    f = open("data/southeast_asia_singular_eej.txt", "a")
    for year in range(2015, 2024):
        for month in range(1, 13):
            local_period = create_month_period(year, month)
            local_start_date, local_end_date = (
                local_period.start,
                local_period.end,
            )
            current_local_date = local_start_date
            while current_local_date <= local_end_date:
                eej = EejDetection([anc, hua], [eus], current_local_date.date())
                if eej.is_singular_eej():
                    f.write(f"{current_local_date.date()}\n")
                current_local_date += timedelta(days=1)
            print("current_date:", current_local_date)
    f.close()
