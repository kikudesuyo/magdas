import pandas as pd
from src.domain.station_params import Period
from src.utils.path import generate_parent_abs_path


class Kp:
    """2000~2022年のKP指数を取得するクラス"""

    def __init__(self):
        path = generate_parent_abs_path("/Storage/kpdata.csv")
        self.df = pd.read_csv(path, parse_dates=["DATETIME_UT"])

    def get_max_of_day(self, ut_period: Period) -> float:

        df_filterd = self.df[
            (self.df["DATETIME_UT"] >= ut_period.start)
            & (self.df["DATETIME_UT"] <= ut_period.end)
        ]
        return df_filterd["kp"].max()
