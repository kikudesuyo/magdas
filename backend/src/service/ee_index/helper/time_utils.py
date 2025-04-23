from datetime import datetime, timedelta

from src.service.ee_index.constant.magdas_station import EeIndexStation
from src.service.ee_index.constant.time_relation import Sec
from src.service.ee_index.helper.params import Period


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
          local_time (datetime.datetime):
        Return:
          ut_time (datetime.datetime): UT time
        """
        time_diff = timedelta(hours=station.time_diff)
        return lt - time_diff

    @staticmethod
    def time_diff(period: Period) -> tuple:
        """Calculate the time difference

        Args:
          start_time (datetime.datetime):
          end_time (datetime.datetime):
        Return:
          (days, hours, minutes) (tuple(int)): time difference
        """
        time_diff = period.end - period.start
        days = time_diff.days
        hours = time_diff.seconds // Sec.ONE_HOUR.const
        minutes = time_diff.seconds % Sec.ONE_HOUR.const // Sec.ONE_MINUTE.const
        return days, hours, minutes
