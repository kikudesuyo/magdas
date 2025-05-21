import datetime
from dataclasses import dataclass
from enum import Enum, IntEnum


class TimeUnit(IntEnum):
    """Time unit in seconds."""

    ONE_MINUTE = 60
    THIRTY_MINUTES = 30 * 60
    ONE_HOUR = 60 * 60
    TWO_HOURS = 2 * 60 * 60
    THREE_HOURS = 3 * 60 * 60
    FIVE_HOURS = 5 * 60 * 60
    SIX_HOURS = 6 * 60 * 60
    FOURTEEN_HOURS = 14 * 60 * 60
    NINETEEN_HOURS = 19 * 60 * 60
    ONE_DAY = 24 * 60 * 60

    @property
    def sec(self) -> int:
        return self.value

    @property
    def min(self) -> int:
        return self.value // 60

    @property
    def hour(self) -> int:
        print("[Log] Time Unit hour property: value be truncated to integer hours")
        return self.value // (60 * 60)


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
