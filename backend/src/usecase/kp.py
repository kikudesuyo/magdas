from datetime import datetime

import pandas as pd
from src.utils.path import generate_parent_abs_path


class Kp:
    """2000~2022年のKP指数を取得するクラス"""

    def __init__(self):
        path = generate_parent_abs_path("/kpdata.csv")
        self.df = pd.read_csv(path, parse_dates=["DATETIME_UT"])

    def get_max(self, start_date: datetime, end_date: datetime) -> float:
        if start_date > end_date:
            raise ValueError("開始日は終了日よりも前の日付である必要があります")
        if start_date < datetime(2000, 1, 1) or end_date > datetime(2022, 12, 31):
            raise ValueError("KP指数は2000年から2022年までのデータしか取得できません")
        df_filterd = self.df[
            (self.df["DATETIME_UT"] >= start_date)
            & (self.df["DATETIME_UT"] <= end_date)
        ]
        return df_filterd["kp"].max()


kp = Kp()
max_kp = kp.get_max(datetime(2021, 12, 31), datetime(2022, 1, 1))
