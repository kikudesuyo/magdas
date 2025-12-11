from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

import numpy as np
from src.domain.station_params import Period, StationParam
from src.service.ee_index.calc.calc_edst import MagdasEdstCalculator
from src.service.ee_index.calc.calc_er import MagdasErCalculator
from src.service.ee_index.calc.calc_euel import ErEdst, MagdasEuelCalculator
from src.service.ee_index.calc.calc_h_component import MagdasHComponent


@dataclass
class EeData:
    euel: np.ndarray
    edst: np.ndarray
    er: np.ndarray
    timeLabels: List[datetime]


class MagdasEeService:
    def __init__(self, ut_params: StationParam) -> None:
        self.ut_params = ut_params

    def calc_all(self) -> EeData:
        h = MagdasHComponent(self.ut_params)
        er = MagdasErCalculator(h.calc_equatorial_h()).calc()
        edst = MagdasEdstCalculator(self.ut_params.period).calc()
        euel = MagdasEuelCalculator(ErEdst(er=er, edst=edst)).calc()
        return EeData(
            er=er,
            edst=edst,
            euel=euel,
            timeLabels=self._minute_labels(),
        )

    def _minute_labels(self) -> List[datetime]:
        return [
            self.ut_params.period.start + timedelta(minutes=i)
            for i in range(self.ut_params.period.total_minutes() + 1)
        ]


class MagdasEuelService:
    def __init__(self, ut_params: StationParam):
        self.ut_params = ut_params

    def calc(self):
        h = MagdasHComponent(self.ut_params)
        er = MagdasErCalculator(h.calc_equatorial_h()).calc()
        edst = MagdasEdstCalculator(self.ut_params.period).calc()
        return MagdasEuelCalculator(ErEdst(er=er, edst=edst)).calc()


class MagdasErService:
    def __init__(self, ut_params: StationParam):
        self.ut_params = ut_params

    def calc(self):
        h = MagdasHComponent(self.ut_params)
        return MagdasErCalculator(h.calc_equatorial_h()).calc()


class MagdasEdstService:
    def __init__(self, period: Period):
        self.period = period

    def calc(self):
        return MagdasEdstCalculator(self.period).calc()
