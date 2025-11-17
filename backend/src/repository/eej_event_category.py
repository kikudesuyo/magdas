import csv
from datetime import datetime
from typing import List

from src.domain.station_params import Period
from src.model.eej_category import EejCategoryModel, EejEventCategory


class EejCategoryRepository:
    def __init__(self):
        self.csv_path = "Storage/eej_category.csv"

    def _fetch_all_from_storage(self) -> List[EejCategoryModel]:
        data: List[EejCategoryModel] = []
        try:
            with open(self.csv_path, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    category_enum = EejEventCategory(row["category"])
                    date = datetime.strptime(row["date"], "%Y-%m-%d").date()
                    data.append(
                        EejCategoryModel(
                            date=date,
                            min_edst=float(row["min_edst"]),
                            kp=float(row["max_kp"]),
                            category=category_enum,
                        )
                    )
        except FileNotFoundError:
            raise FileNotFoundError(f"{self.csv_path} not found.")
        return data

    def select(self, period: Period, category: str) -> List[EejCategoryModel]:
        """条件に応じて絞り込み"""
        data = self._fetch_all_from_storage()  # ← CSV/DB/Firestore など、取得元は自由
        result = []
        start_date = period.start
        end_date = period.end

        for row in data:
            if category is not None and row.category.value != category:
                continue
            if start_date is not None and row.date < start_date.date():
                continue
            if end_date is not None and row.date > end_date.date():
                continue
            result.append(row)
        return result
