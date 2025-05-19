import datetime
from dataclasses import dataclass
from enum import Enum, IntEnum


class Min(IntEnum):
    ONE_HOUR = 60
    THREE_HOURS = 180
    SIX_HOURS = 360
    ONE_DAY = 1440
    FIVE_DAYS = 7200
    THIRTY_DAYS = 43200
    SIXTY_DAYS = 86400


class Sec(IntEnum):
    ONE_DAY = 86400
    ONE_HOUR = 3600
    ONE_MINUTE = 60


@dataclass
class TimeRange:
    start: datetime.time
    end: datetime.time

    def contains(self, time: datetime.time) -> bool:
        """Check if the given time is within the range."""
        if self.start <= self.end:
            return self.start <= time <= self.end
        else:
            return self.start <= time or time <= self.end


class DawnAndDusk(TimeRange, Enum):
    DAYSIDE = (
        datetime.time(6, 0, 0),
        datetime.time(17, 59, 59),
    )
    NIGHTSIDE = (
        datetime.time(18, 0, 0),
        datetime.time(5, 59, 59),
    )
