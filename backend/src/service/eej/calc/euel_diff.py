from datetime import date, datetime, time, timedelta

import numpy as np
from src.constants.time_relation import (
    EEJ_DETECTION_END_TIME,
    EEJ_DETECTION_START_TIME,
    TimeUnit,
)
from src.model.euel_data import EuelData


class DaytimeInterval:
    @classmethod
    def contains(cls, t: time) -> bool:
        return EEJ_DETECTION_START_TIME <= t <= EEJ_DETECTION_END_TIME


def calc_euel_peak_diff(
    dip_euel: EuelData, offdip_euel: EuelData, local_date: date
) -> float:
    timestamp = np.array(
        [
            datetime(local_date.year, local_date.month, local_date.day, 0, 0)
            + timedelta(minutes=i)
            for i in range(TimeUnit.ONE_DAY.min)
        ]
    )
    is_noon = np.array([DaytimeInterval.contains(dt.time()) for dt in timestamp])

    if (
        np.isnan(dip_euel.array[is_noon]).all()
        or np.isnan(offdip_euel.array[is_noon]).all()
    ):
        return float("nan")
    dip_max = np.max(dip_euel.array[is_noon])
    offdip_max = np.max(offdip_euel.array[is_noon])
    return float(dip_max - offdip_max)
