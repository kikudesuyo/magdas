from dataclasses import dataclass
from datetime import datetime

import numpy as np
from numpy.typing import NDArray
from src.constants.time_relation import TimeUnit
from src.domain.magdas_station import EeIndexStation
from src.utils.date import DateUtils


@dataclass
class Period:
    start: datetime
    end: datetime

    def __post_init__(self):
        if self.start >= self.end:
            raise ValueError("Start time must be before end time.")
        if self.start.second != 0 or self.start.microsecond != 0:
            raise ValueError("Start time must be minute-precision (no seconds).")
        if self.end.second != 0 or self.end.microsecond != 0:
            raise ValueError("End time must be minute-precision (no seconds).")

    def total_minutes(self) -> int:
        return int((self.end - self.start).total_seconds() // TimeUnit.ONE_MINUTE.sec)

    def time_diff(self) -> tuple[int, int, int]:
        """Return (days, hours, minutes) of the period."""
        diff = self.end - self.start
        days = diff.days
        # timedelta.seconds は 日数を除いた部分(0 ~86399秒)を返す
        seconds = diff.seconds
        hours, r = divmod(seconds, TimeUnit.ONE_HOUR.sec)
        minutes, _ = divmod(r, TimeUnit.ONE_MINUTE.sec)
        return days, hours, minutes

    def get_minute_list(self) -> NDArray[np.datetime64]:
        start = np.datetime64(self.start, "m")
        length = self.total_minutes() + 1  # include start and end
        return np.array(
            [start + np.timedelta64(i, "m") for i in range(length)],
            dtype="datetime64[m]",
        )


@dataclass
class StationParam:
    station: EeIndexStation
    period: Period

    def to_ut_params(self):
        """Convert to UT params"""
        start_ut = DateUtils.to_ut(self.station, self.period.start).replace(
            second=0, microsecond=0
        )
        end_ut = DateUtils.to_ut(self.station, self.period.end).replace(
            second=0, microsecond=0
        )
        return StationParam(self.station, Period(start_ut, end_ut))
