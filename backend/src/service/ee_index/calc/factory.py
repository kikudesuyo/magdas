from datetime import datetime

from src.service.ee_index.calc.edst_index import Edst
from src.service.ee_index.calc.er_value import Er, NightEr

# from src.service.ee_index.calc.euel_index import EuelCalc
from src.service.ee_index.calc.h_component_extraction import HComponent
from src.service.ee_index.calc.params import CalcParams, Period
from src.service.ee_index.constant.magdas_station import EeIndexStation


class EeFactory:
    def __init__(
        self,
        station: EeIndexStation,
        start_ut: datetime,
        end_ut: datetime,
    ):
        period = Period(start_ut, end_ut)
        params = CalcParams(station, period)
        self.station = station
        self.start_ut = start_ut
        self.end_ut = end_ut

        self.h = HComponent(params)
        self.er = Er(self.h)
        self.night_er = NightEr(params)
        self.edst = Edst(period)
        # self.euel = EuelCalc(self.er, self.edst)
