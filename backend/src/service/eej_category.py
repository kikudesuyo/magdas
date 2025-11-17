from typing import List

from src.domain.station_params import Period
from src.model.eej_category import EejCategoryModel
from src.repository.eej_event_category import EejCategoryRepository


class EejCategoryService:
    def __init__(self):
        self.repository = EejCategoryRepository()

    def get_category_by_period_and_type(
        self, period: Period, eej_type: str
    ) -> List[EejCategoryModel]:
        categories = self.repository.select(period=period, category=eej_type)
        if not categories:
            raise ValueError(
                f"No category found for type {eej_type} in period {period}."
            )
        return categories
