import calendar
from datetime import datetime, timedelta

from src.ee_index.constant.magdas_station import EeIndexStation
from src.ee_index.constant.time_relation import Day, Sec


class DateUtils:
    @staticmethod
    def get_days_in_month(year, month) -> int:
        """Get the number of days in the month
        Args:
          year (int):
          month (int):
        Return:
          days (int): number of days in the month
        """
        days = calendar.monthrange(year, month)[1]
        return days

    @staticmethod
    def get_days_in_year(year) -> int:
        """Get the number of days in the year
        Args:
          year (int):
        Return:
          days (int): number of days in the year
        """
        days = Day.IN_NON_LEAP_YEAR.const
        if calendar.isleap(year):
            days = Day.IN_LEAP_YEAR.const
        return days

    @staticmethod
    def to_local_time(station, ut_time: datetime) -> datetime:
        """Convert to local time
        Args:
          station (str):
          ut_time (datetime.datetime):
        Return:
          local_time (datetime.datetime): local time
        """
        time_diff = timedelta(hours=EeIndexStation[station].time_diff)
        local_time = ut_time + time_diff
        return local_time

    @staticmethod
    def to_ut_time(station, local_time: datetime) -> datetime:
        """Convert to UT time
        Args:
          station (str):
          local_time (datetime.datetime):
        Return:
          ut_time (datetime.datetime): UT time
        """
        time_diff = timedelta(hours=EeIndexStation[station].time_diff)
        ut_time = local_time - time_diff
        return ut_time

    @staticmethod
    def time_diff(start_time: datetime, end_time: datetime) -> tuple:
        """Calculate the time difference

        Args:
          start_time (datetime.datetime):
          end_time (datetime.datetime):
        Return:
          (days, hours, minutes) (tuple(int)): time difference
        """
        time_diff = end_time - start_time
        days = time_diff.days
        hours = time_diff.seconds // Sec.ONE_HOUR.const
        minutes = time_diff.seconds % Sec.ONE_HOUR.const // Sec.ONE_MINUTE.const
        return days, hours, minutes

    @staticmethod
    def get_day_start(input_datetime: datetime) -> datetime:
        """Get the start time of the day

        Args:
          datetime (datetime.datetime):
        Return:
          datetime (datetime.datetime): start time of the day
        """
        return datetime.replace(input_datetime, hour=0, minute=0, second=0)
