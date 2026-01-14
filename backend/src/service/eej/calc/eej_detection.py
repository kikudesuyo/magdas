from datetime import date, datetime
from typing import Literal

import numpy as np
from pydantic import BaseModel
from src.constants.ee_index import (
    BRAZIL_LOWER_10_PERCENTILE_THRESHOLD,
    SOUTH_AMERICA_LOWER_10_PERCENTILE_THRESHOLD,
)
from src.domain.region import Region
from src.domain.station_params import Period
from src.service.ee_index.magdas_ee import MagdasEdstService
from src.service.kp import Kp


class EejCategory(BaseModel):
    label: Literal[
        "peculiar",  # 特異型EEJ: peculiar
        "normal",  # 通常型EEJ: normal
        "disturbance",  # 擾乱(Kp指数とEDstで判断): disturbance
        "missing",  # データ欠測: missing
    ]

    @classmethod
    def from_conditions(
        cls,
        peak_diff: float,
        daily_max_kp: float,
        daily_min_edst: float,
        region: Region,
    ) -> "EejCategory":
        if daily_max_kp >= 4 or daily_min_edst < -30:
            return cls(label="disturbance")
        if np.isnan(peak_diff):
            return cls(label="missing")
        if region == Region.SOUTH_AMERICA:
            if peak_diff >= SOUTH_AMERICA_LOWER_10_PERCENTILE_THRESHOLD:
                return cls(label="normal")
            return cls(label="peculiar")
        elif region == Region.BRAZIL:
            if peak_diff >= BRAZIL_LOWER_10_PERCENTILE_THRESHOLD:
                return cls(label="normal")
            return cls(label="peculiar")
        else:
            raise ValueError(f"Unsupported region: {region}")


class EejDetection:
    def __init__(self, euel_peak_diff: float, local_date: date, region: Region):
        self.local_date = local_date
        self.euel_peak_diff = euel_peak_diff
        self.region = region

    def _calc_daily_min_edst(self):
        s_dt = datetime(
            self.local_date.year, self.local_date.month, self.local_date.day, 0, 0
        )
        e_dt = s_dt.replace(hour=23, minute=59)
        period = Period(s_dt, e_dt)
        edst_service = MagdasEdstService(period)
        edst = edst_service.calc()
        return np.min(edst)

    def _get_daily_max_kp(self):
        ut_period = Period(
            datetime(
                self.local_date.year, self.local_date.month, self.local_date.day, 0, 0
            ),
            datetime(
                self.local_date.year, self.local_date.month, self.local_date.day, 23, 59
            ),
        )
        kp = Kp().get_max_of_day(ut_period)
        return kp

    def classify_eej_category(self) -> EejCategory:
        daily_max_kp = self._get_daily_max_kp()
        daily_min_edst = self._calc_daily_min_edst()
        return EejCategory.from_conditions(
            peak_diff=self.euel_peak_diff,
            daily_max_kp=daily_max_kp,
            daily_min_edst=daily_min_edst,
            region=self.region,
        )
