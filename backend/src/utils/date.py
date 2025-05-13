from datetime import datetime, timedelta

from src.usecase.ee_index.constant.magdas_station import EeIndexStation


def to_datetime(date: str) -> datetime:
    """Converts a string to a date object"""
    return datetime.strptime(date, "%Y-%m-%d")


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
