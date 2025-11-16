from typing import Optional

import pandas as pd
from src.utils.path import generate_parent_abs_path


class StationData:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path, parse_dates=["date"])

    def query(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        station_code: Optional[str] = None,
    ) -> pd.DataFrame:
        df = self.df
        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]
        if station_code:
            df = df[df["station_code"] == station_code]
        return df.reset_index(drop=True)


if __name__ == "__main__":
    path = generate_parent_abs_path(
        "/Storage/peak_euel/southeast_asia_dip_station_peak_euel.csv"
    )
    data = StationData(path)
    result = data.query(
        start_date="2000-01-01", end_date="2000-01-10", station_code="BCL"
    )
    print(result)
