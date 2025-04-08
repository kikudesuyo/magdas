from datetime import time

EEJ_THRESHOLD = 10


class EejDetectionTime:
    START = time(10, 0)
    END = time(13, 59)

    @classmethod
    def contains(cls, t: time) -> bool:
        return cls.START <= t <= cls.END
