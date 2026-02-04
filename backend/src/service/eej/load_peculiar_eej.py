import csv
from datetime import date
from typing import List

from src.domain.region import Region
from src.utils.path import generate_parent_abs_path


def load_peculiar_eej_dates(region: Region) -> List[date]:
    peculiar_eej_dates: List[date] = []
    if region != Region.BRAZIL:
        raise ValueError("Currently, only Region.BRAZIL is supported.")

    path = generate_parent_abs_path("/Storage/peculiar_eej/peculiar_eej_types.csv")
    with open(path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["classification"] != "peculiar":
                continue
            year, month, day = map(int, row["date"].split("-"))
            peculiar_eej_dates.append(date(year, month, day))

    return peculiar_eej_dates
