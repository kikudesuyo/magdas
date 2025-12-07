from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from pydantic import BaseModel
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period


class KatoEeData(BaseModel):
    dt: datetime
    euel_data: float
    edst_data: float


class KatoEeRepository:
    def __init__(self, station: EeIndexStation):
        self.station = station
        self.station_dir_path = Path(f"Storage/kato/{station.code}")

        if not self.station_dir_path.exists():
            raise ValueError(f"Station directory not found: {self.station_dir_path}")

    def select_by_range(self, period: Period) -> list[KatoEeData]:
        """
        日毎のCSVを対象に、指定期間のEE指数データを取得
        """
        result: list[KatoEeData] = []

        for target_date in self._iter_dates(period.start, period.end):
            csv_path = self._build_daily_path(target_date)

            if not csv_path.exists():
                continue

            for chunk in pd.read_csv(
                csv_path,
                parse_dates=["DATETIME"],
                na_values=["", " "],
                dtype={"EUEL1m": "float64", "EDst1m": "float64"},
                chunksize=200_000,
            ):
                filtered = chunk[
                    (chunk["DATETIME"] >= period.start)
                    & (chunk["DATETIME"] <= period.end)
                ]

                if filtered.empty:
                    continue

                result.extend(
                    KatoEeData(
                        dt=row.DATETIME,
                        euel_data=row.EUEL1m,
                        edst_data=row.EDst1m,
                    )
                    for row in filtered.itertuples(index=False)
                )

        return result

    def _iter_dates(self, start: datetime, end: datetime):
        current = start.date()
        last = end.date()

        while current <= last:
            yield current
            current += timedelta(days=1)

    def _build_daily_path(self, date_obj) -> Path:
        date_str = date_obj.strftime("%Y%m%d")
        filename = f"{self.station.code}_{date_str}.csv"
        return self.station_dir_path / filename
