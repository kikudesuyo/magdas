from datetime import datetime, timedelta

import numpy as np
from numpy.typing import NDArray
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period


def str_to_datetime(str_date: str) -> datetime:
    """Converts a string to a date object"""
    return datetime.strptime(str_date, "%Y-%m-%d")


def get_minute_list(period: Period) -> NDArray[np.datetime64]:
    start = np.datetime64(period.start, "m")
    length = period.total_minutes() + 1  # include start and end
    return np.array(
        [start + np.timedelta64(i, "m") for i in range(length)], dtype="datetime64[m]"
    )


class DateUtils:

    @staticmethod
    def to_lt(station: EeIndexStation, ut: datetime) -> datetime:
        """Convert to local time
        Args:
          station (str):
          ut (datetime.datetime): universal time
        Return:
          lt (datetime.datetime): local time
        """
        time_diff = timedelta(hours=station.time_diff)
        return ut + time_diff

    @staticmethod
    def to_ut(station: EeIndexStation, lt: datetime) -> datetime:
        """Convert to UT time
        Args:
          station (str):
          lt(datetime.datetime): local time
        Return:
          ut (datetime.datetime): universal time
        """
        time_diff = timedelta(hours=station.time_diff)
        return lt - time_diff
