from dataclasses import dataclass

KP_QUIET_THRESHOLD = 4
EDST_QUIET_THRESHOLD = -30


@dataclass(frozen=True)
class QuietDayDomain:
    min_edst: float
    max_kp: float

    def is_quiet_day(self) -> bool:
        return (
            self.min_edst >= EDST_QUIET_THRESHOLD and self.max_kp < KP_QUIET_THRESHOLD
        )
