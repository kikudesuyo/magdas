from datetime import datetime, time, timedelta

import numpy as np
from src.ee_index.calc.h_component_extraction import HComponent
from src.ee_index.constant.er_threshold import MAX_ER_VALUE, MIN_ER_VALUE
from src.ee_index.constant.time_relation import DawnAndDusk, Day, DayTimeRange, Min
from src.ee_index.helper.time_utils import DateUtils
from src.ee_index.helper.warnings_suppression import NanCalculator


class HComponentDelegate:
    def __init__(self, station, datetime: datetime):
        self.station, self.datetime = station, datetime
        self.component = HComponent()

    def get_h_component_for_days(self, days):
        # return self.component.get_h_for_days(self.station, self.datetime, days)
        return self.component.interpolate_h_component(self.station, self.datetime, days)


class Er:
    def __init__(self, station, datetime: datetime):
        self.station, self.datetime = station, datetime

    def get_h_component(self, datetime, days):
        h_component_delegate = HComponentDelegate(self.station, datetime)
        return h_component_delegate.get_h_component_for_days(days)

    def calc_er_base_value(self, days) -> np.ndarray:
        """Callculate the daily median of the h component for ER calculation"""
        h_component = self.get_h_component(DateUtils.get_day_start(self.datetime), days)
        base_values = np.array([], dtype=np.float32)
        for day in range(days):
            start_index = day * Min.ONE_DAY.const
            end_index = start_index + Min.ONE_DAY.const - 1
            daily_h_component = h_component[start_index : end_index + 1]
            base_values = np.append(
                base_values, NanCalculator.nanmedian(daily_h_component)
            )
        base_values = np.array(base_values, dtype=np.float32)
        return base_values

    def calc_er_for_days(self, days):
        h_component = self.get_h_component(self.datetime, days)
        base_values = self.calc_er_base_value(days)
        # TODO: Refactor this part 正しくベースラインを引けていない 1日の途中から開始すると値がずれる
        tiled_base_values = np.repeat(base_values, Min.ONE_DAY.const)
        er = h_component - tiled_base_values
        interpolated_er = self.remove_er_outliers(er)
        return interpolated_er

    def calc_er_for_min(self, time: time) -> np.float32:
        """Calculate ER value for a specific minute."""
        er_value = self.calc_er_for_days(Day.ONE.const)
        array_index = time.hour * Min.ONE_HOUR.const + time.minute
        er_value = er_value[array_index]
        return er_value

    def remove_er_outliers(self, rough_er: np.ndarray) -> np.ndarray:
        """Remove outliers from ER value"""
        rough_er[rough_er > MAX_ER_VALUE] = np.nan
        rough_er[rough_er < MIN_ER_VALUE] = np.nan
        return rough_er


class ErEDstConnecter:
    """EDst指数は1日の途中から開始される場合があるため再定義する必要がある。
    e.g.) 2010/4/1 8:00 ~ 2010/4/2 7:59のEDst指数を計算:
    ER値のベースラインの計算: 2010/4/1 0:00 ~ 2010/4/1 23:59 と 2010/4/2 0:00 ~ 2010/4/2 23:59 で算出 -> [4/1のベースライン, 4/2のベースライン]
    ER値の計算: 対応する時刻のベースラインを引く -> [4/1 8:00のER値, 4/1 8:01のER値, ..., 4/2 7:59のER値]
    """

    def __init__(self, station):
        self.station = station

    def calc_er_for_part_of_a_day(
        self, start_datetime: datetime, end_time: time
    ) -> np.ndarray:
        """Calculate ER value for a specific part of day."""
        all_er_value = Er(
            self.station, DateUtils.get_day_start(start_datetime)
        ).calc_er_for_days(Day.ONE.const)
        array_index_start = (
            start_datetime.hour * Min.ONE_HOUR.const + start_datetime.minute
        )
        array_index_end = end_time.hour * Min.ONE_HOUR.const + end_time.minute
        part_er_value = all_er_value[array_index_start : array_index_end + 1]
        return part_er_value

    def calc_full_er(self, start_full_datetime: datetime, full_days: int):
        """一日分のER値を計算"""
        if full_days == 0:
            return np.array([])
        full_er = Er(self.station, start_full_datetime).calc_er_for_days(full_days)
        return full_er

    def get_er_for_edst(self, start_datetime: datetime, days: int) -> np.ndarray:
        """Redefine the baseline on a daily basis and calculate ER value"""
        if start_datetime.time() == time(0, 0):
            # "緯度0度の観測点でのer値"
            er = Er(self.station, start_datetime).calc_er_for_days(days)
            return er
        end_datetime = start_datetime + timedelta(days=days, minutes=-1)
        head_er = self.calc_er_for_part_of_a_day(start_datetime, DayTimeRange.DAY.end)
        full_er = self.calc_full_er(
            DateUtils.get_day_start(start_datetime) + timedelta(days=1), days - 1
        )
        foot_er = self.calc_er_for_part_of_a_day(
            DateUtils.get_day_start(end_datetime),
            end_datetime.time(),
        )
        er = np.concatenate((head_er, full_er, foot_er))
        return er


class NightEr(ErEDstConnecter):
    """
    TODO: This class is needed to be refactored.
    """

    def __init__(self, station, datetime, days: int):
        super().__init__(station)
        self.datetime = datetime
        self.days = days

    def get_corresponding_local_time(self) -> np.ndarray:
        local_datetime = DateUtils.to_local_time(self.station, self.datetime)
        return np.array(
            [
                (local_datetime + timedelta(minutes=i)).time()
                for i in range(Min.ONE_DAY.const * self.days)
            ]
        )

    def is_daytime(self) -> np.ndarray:
        condition = np.logical_and(
            DawnAndDusk.DAYSIDE.start <= self.get_corresponding_local_time(),
            self.get_corresponding_local_time() <= DawnAndDusk.DAYSIDE.end,
        )
        return condition

    def extract_night_er(self) -> np.ndarray:
        condition = self.is_daytime()
        night_er = np.vstack(
            np.where(
                condition, np.nan, super().get_er_for_edst(self.datetime, self.days)
            )
        ).ravel()
        return night_er
