from src.domain.station_params import Period, StationParams
from src.usecase.ee_index.calc_edst import Edst
from src.usecase.ee_index.calc_er import Er
from src.usecase.ee_index.calc_euel import Euel
from src.usecase.ee_index.calc_h_component import HComponent


class EeFactory:
    def create_h(self, calc_params: StationParams):
        return HComponent(calc_params)

    def create_er(self, calc_params: StationParams):
        h = self.create_h(calc_params)
        return Er(h)

    def create_edst(self, period: Period):
        return Edst(period)

    def create_euel(self, calc_params: StationParams):
        er = self.create_er(calc_params)
        edst = self.create_edst(calc_params.period)
        return Euel(er, edst)
