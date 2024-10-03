from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from util import generate_abs_path


def read_iaga_data(abs_path):
    df = pd.read_table(
        abs_path,
        sep="\s+",
        skiprows=13,
        names=["DATE", "TIME", "DOY", "EDst1h", "EDst6h", "ER", "EUEL"],
    )
    return df


def get_iaga_ee_for_days(station, start_datetime: datetime, days: int):
    initial_datetime = start_datetime
    er_days, edst_days, euel_days = (
        np.array([]),
        np.array([]),
        np.array([]),
    )
    for day in range(days):
        date = (initial_datetime + timedelta(days=day)).date()
        abs_path = generate_abs_path(
            f"/2014/EEindex{date.strftime('%Y%m%d')}pmin.{station}"
        )
        df = read_iaga_data(abs_path)
        er, edst, euel = (df["ER"], df["EDst1h"], df["EUEL"])
        er_days = np.concatenate((er_days, er))
        edst_days = np.concatenate((edst_days, edst))
        euel_days = np.concatenate((euel_days, euel))
    ee = np.array([er_days, edst_days, euel_days])
    return ee
