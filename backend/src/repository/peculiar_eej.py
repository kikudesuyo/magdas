import csv
from datetime import date, datetime
from typing import List

from pydantic import BaseModel
from src.domain.region import Region


class PeculiarEej(BaseModel):
    date: date
    region: Region


class PeculiarEejRepository:
    def __init__(self):
        self.csv_path = "Storage/peculiar.csv"

    def select_all(self) -> List[PeculiarEej]:
        data: List[PeculiarEej] = []
        try:
            with open(self.csv_path, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    region_enum = Region.from_code(row["region"])
                    date = datetime.strptime(row["date"], "%Y-%m-%d").date()
                    data.append(PeculiarEej(date=date, region=region_enum))

        except FileNotFoundError:
            raise FileNotFoundError(f"{self.csv_path} not found.")
        return data

    def select_by_region(self, region: Region) -> List[date]:
        data = self.select_all()
        return [row.date for row in data if row.region == region]

    def insert(self, row: PeculiarEej) -> None:
        file_exists = False
        try:
            with open(self.csv_path, "r", encoding="utf-8"):
                file_exists = True
        except FileNotFoundError:
            pass

        with open(self.csv_path, mode="a", newline="", encoding="utf-8") as f:
            fieldnames = ["date", "region"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow({"date": row.date, "region": row.region.code})
