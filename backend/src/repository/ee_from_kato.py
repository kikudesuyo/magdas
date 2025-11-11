from datetime import datetime

import pandas as pd
from domain.station_params import Period
from pydantic import BaseModel


class KatoEeData(BaseModel):
    dt: datetime
    euel_data: float
    edst_data: float


class KatoEeRepository:
    STATION_PATHS = {
        "EUS": "Storage/kato/EUS_EUEL.csv",
        "TTB": "Storage/kato/TTB_EUEL.csv",
        "KOU": "Storage/kato/KOU_EUEL.csv",
    }

    def __init__(self, station_code: str):
        if station_code not in self.STATION_PATHS:
            raise ValueError(f"Unsupported station code: {station_code}")
        self.csv_path = self.STATION_PATHS[station_code]

    def select_by_range(self, period: Period) -> list[KatoEeData]:
        result: list[KatoEeData] = []

        for chunk in pd.read_csv(
            self.csv_path,
            parse_dates=["DATETIME"],
            na_values=["", " "],
            dtype={"EUEL1m": "float64", "EDst1m": "float64"},
            chunksize=200_000,
        ):
            filtered = chunk[
                (chunk["DATETIME"] >= period.start) & (chunk["DATETIME"] <= period.end)
            ]
            if filtered.empty:
                continue

            result.extend(
                KatoEeData(dt=row.DATETIME, euel_data=row.EUEL1m, edst_data=row.EDst1m)
                for row in filtered.itertuples(index=False)
            )

        return result
