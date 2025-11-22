import csv
import os
from datetime import date, datetime
from typing import List

from src.domain.region import Region
from src.model.peculiar_eej import PeculiarEejModel


# 特異型EEJを保存・取得するリポジトリ層
class PeculiarEejRepository:
    def __init__(self):
        self.csv_path = "Storage/peculiar_eej_classification.csv"

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
        # 既存データの取得
        try:
            existing_data = self._fetch_all_from_storage()
        except FileNotFoundError:
            existing_data = []

        existing_map: dict[tuple[date, Region], str] = {
            (row.date, row.region): row.type for row in existing_data
        }
        new_data: List[PeculiarEejModel] = []

        for row in rows:
            key = (row.date, row.region)

            if key in existing_map:
                # 既存データとタイプが異なる場合はエラー
                if existing_map[key] != row.type:
                    raise ValueError(
                        f"Conflicting data found: "
                        f"Date={row.date}, Region={row.region.code}, "
                        f"Existing Type={existing_map[key]}, New Type={row.type}"
                    )
                # 既存のデータと同じ
                print("[Info] Duplicate skipping:", row.date, row.region.code, row.type)
                continue

            # 新しいデータ
            new_data.append(row)

        # 追加なしなら終了
        if not new_data:
            return

        file_exists = os.path.exists(self.csv_path)

        with open(
            self.csv_path,
            mode="a" if file_exists else "w",
            newline="",
            encoding="utf-8",
        ) as f:
            writer = csv.DictWriter(f, fieldnames=["Date", "Region", "Type"])

            if not file_exists:
                writer.writeheader()

            for row in new_data:
                writer.writerow(
                    {"Date": row.date, "Region": row.region.code, "Type": row.type}
                )
