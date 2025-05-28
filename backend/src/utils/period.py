import calendar
from datetime import datetime

import numpy as np
from numpy.typing import NDArray
from src.domain.station_params import Period


def create_month_period(year: int, month: int) -> Period:
    """Convert a period to a monthly period"""
    last_day = calendar.monthrange(year, month)[1]
    return Period(
        start=datetime(year, month, 1, 0, 0),
        end=datetime(year, month, last_day, 23, 59),
    )


def get_minute_list(period: Period) -> NDArray[np.datetime64]:
    start = np.datetime64(period.start, "m")
    length = period.total_minutes() + 1  # include start and end
    return np.array(
        [start + np.timedelta64(i, "m") for i in range(length)], dtype="datetime64[m]"
    )
