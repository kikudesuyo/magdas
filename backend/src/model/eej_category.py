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
