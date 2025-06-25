from datetime import datetime

import pandas as pd
from src.utils.path import generate_parent_abs_path


class Kp:
    """2000~2022年のKP指数を取得するクラス"""

    def __init__(self):
        path = generate_parent_abs_path("/Storage/kpdata.csv")
        self.df = pd.read_csv(path, parse_dates=["DATETIME_UT"])

    def get_max_of_day(self, start_dt: datetime, end_dt: datetime) -> float:
        if start_dt > end_dt:
            raise ValueError("開始日は終了日よりも前の日付である必要があります")
        if start_dt < datetime(2000, 1, 1) or end_dt > datetime(2022, 12, 31):
            raise ValueError("KP指数は2000年から2022年までのデータしか取得できません")
        df_filterd = self.df[
            (self.df["DATETIME_UT"] >= start_dt) & (self.df["DATETIME_UT"] <= end_dt)
        ]
        return df_filterd["kp"].max()


if __name__ == "__main__":
    kp = Kp()
    max_kp = kp.get_max_of_day(datetime(2021, 12, 31), datetime(2022, 1, 1))
