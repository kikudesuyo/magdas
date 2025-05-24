import calendar
from datetime import datetime

from src.domain.station_params import Period


def create_month_period(year: int, month: int) -> Period:
    """Convert a period to a monthly period"""
    last_day = calendar.monthrange(year, month)[1]
    return Period(
        start=datetime(year, month, 1, 0, 0),
        end=datetime(year, month, last_day, 23, 59),
    )
