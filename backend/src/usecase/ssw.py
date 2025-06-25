from datetime import datetime

import pandas as pd
from src.utils.path import generate_parent_abs_path


class Ssw:
    def __init__(self):
        path = generate_parent_abs_path("/Storage/ssw_2000-2024.csv")
        self.df = pd.read_csv(path, parse_dates=["Date"])

    def get_ssw_by_range(self, start_dt: datetime, end_dt: datetime) -> pd.DataFrame:
        if start_dt > end_dt:
            raise ValueError("開始日は終了日よりも前の日付である必要があります")
        if start_dt < datetime(2000, 1, 1) or end_dt > datetime(2024, 12, 31):
            raise ValueError("SSW指数は2000年から2024年までのデータしか取得できません")
        self.df["Date"] = pd.to_datetime(self.df["Date"], format="mixed")

        return self.df[
            (self.df["Date"] >= start_dt) & (self.df["Date"] <= end_dt)
        ].reset_index(drop=True)
