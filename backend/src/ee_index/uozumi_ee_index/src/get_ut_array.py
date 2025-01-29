from datetime import datetime, timedelta

import numpy as np


def get_ut_array(start_datetime: datetime, days):
    minutes = 60 * 24 * days
    ut_array = np.array(
        [start_datetime + timedelta(minutes=minute) for minute in range(minutes)]
    )
    return ut_array
