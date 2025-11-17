import csv
import os
from datetime import datetime
from typing import List

from src.domain.region import Region
from src.model.peculiar_eej import PeculiarEejModel


# 特異型EEJを保存・取得するリポジトリ層
class PeculiarEejRepository:
    def __init__(self):
        self.csv_path = "Storage/test_from_2009_to_2020.csv"

    def _fetch_all_from_storage(self) -> List[PeculiarEejModel]:
        data: List[PeculiarEejModel] = []
        try:
            with open(self.csv_path, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    region_enum = Region.from_code(row["Region"])
                    date = datetime.strptime(row["Date"], "%Y-%m-%d").date()
                    data.append(
                        PeculiarEejModel(
                            date=date, region=region_enum, type=row["Type"]
                        )
                    )

        except FileNotFoundError:
            raise FileNotFoundError(f"{self.csv_path} not found.")
        return data

    def select(
        self,
        region: Region | None = None,
        type_: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> list[PeculiarEejModel]:
        """条件に応じて絞り込み"""
        data = self._fetch_all_from_storage()  # ← CSV/DB/Firestore など、取得元は自由
        result = []

        for row in data:
            if region is not None and row.region != region:
                continue
            if type_ is not None and row.type != type_:
                continue
            if start_date is not None and row.date < start_date.date():
                continue
            if end_date is not None and row.date > end_date.date():
                continue
            result.append(row)
        return result

    def insert(self, rows: List[PeculiarEejModel]) -> None:
        # 既存データのチェック
        if os.path.exists(self.csv_path):
            raise FileExistsError(f"{self.csv_path} already exists.")

        with open(self.csv_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Date", "Region", "Type"])
            writer.writeheader()
            for row in rows:
                writer.writerow(
                    {"Date": row.date, "Region": row.region.code, "Type": row.type}
                )
