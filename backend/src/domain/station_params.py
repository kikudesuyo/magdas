from dataclasses import dataclass
from datetime import datetime

from src.constants.magdas_station import EeIndexStation
from src.constants.time_relation import Sec
from src.utils.date import DateUtils


@dataclass
class Period:
    start: datetime
    end: datetime

    def __post_init__(self):
        if self.start >= self.end:
            raise ValueError("Start time must be before end time.")

    def time_diff(self) -> tuple[int, int, int]:
        """Calculate the time difference

        Args:
          start_time (datetime.datetime):
          end_time (datetime.datetime):
        Return:
          (days, hours, minutes) (tuple(int)): time difference
        """
        time_diff = self.end - self.start
        days = time_diff.days
        hours = time_diff.seconds // Sec.ONE_HOUR.const
        minutes = time_diff.seconds % Sec.ONE_HOUR.const // Sec.ONE_MINUTE.const
        return days, hours, minutes


@dataclass
class StationParams:
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
        return StationParams(self.station, Period(start_ut, end_ut))
