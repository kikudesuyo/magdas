from datetime import date, datetime
from typing import Literal

import numpy as np
from pydantic import BaseModel
from src.constants.ee_index import EEJ_THRESHOLD
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
    ) -> "EejCategory":
        if daily_max_kp >= 4 or daily_min_edst < -30:
            return cls(label="disturbance")
        if np.isnan(peak_diff):
            return cls(label="missing")
        if peak_diff >= EEJ_THRESHOLD:
            return cls(label="normal")
        return cls(label="peculiar")


class EejDetection:
    def __init__(self, euel_peak_diff: float, local_date: date):
        self.local_date = local_date
        self.euel_peak_diff = euel_peak_diff

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

    def is_eej_peak_diff_nan(self):
        """データ欠損か判定"""
        return np.isnan(self.euel_peak_diff)

    def is_eej_present(self):
        return self.euel_peak_diff >= EEJ_THRESHOLD

    def is_peculiar_eej(self):
        return self.classify_eej_category().label == "peculiar"

    def classify_eej_category(self) -> EejCategory:
        daily_max_kp = self._get_daily_max_kp()
        daily_min_edst = self._calc_daily_min_edst()
        return EejCategory.from_conditions(
            peak_diff=self.euel_peak_diff,
            daily_max_kp=daily_max_kp,
            daily_min_edst=daily_min_edst,
        )
