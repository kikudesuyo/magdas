import datetime
from dataclasses import dataclass
from enum import Enum


@dataclass
class TimeConst:
    const: int


class Day(TimeConst, Enum):
    ONE = 1
    IN_LEAP_YEAR = 366
    IN_NON_LEAP_YEAR = 365


class Min(TimeConst, Enum):
    ONE_HOUR = 60
    THREE_HOURS = 180
    ONE_DAY = 1440
    FIVE_DAYS = 7200
    THIRTY_DAYS = 43200
    SIXTY_DAYS = 86400


class Sec(TimeConst, Enum):
    ONE_DAY = 86400
    ONE_HOUR = 3600
    ONE_MINUTE = 60


@dataclass
class TimeRange:
    start: datetime.time
    end: datetime.time


class DawnAndDusk(TimeRange, Enum):
    DAYSIDE = (
        datetime.time(6, 0, 0),
        datetime.time(17, 59, 59),
    )
    NIGHTSIDE = (
        datetime.time(18, 0, 0),
        datetime.time(5, 59, 59),
    )


class DayTimeRange(TimeRange, Enum):
    DAY = (
        datetime.time(0, 0, 0),
        datetime.time(23, 59, 59),
    )
