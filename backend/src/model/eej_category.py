from datetime import date
from enum import Enum

from pydantic import BaseModel


class EejEventCategory(str, Enum):
    QUIET = "quiet"
    DISTURBANCE = "disturbance"
    MISSING = "missing"

    @property
    def label(self):
        return self.value


class EejCategoryModel(BaseModel):
    date: date
    min_edst: float
    kp: float
    category: EejEventCategory


class PeculiarEejType(str, Enum):
    UNDEVELOPED = "未発達型"
    SUDDEN = "突発型"
    ERROR = "エラー"
