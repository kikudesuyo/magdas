from src.usecase.ee_index.calc.edst import Edst
from src.usecase.ee_index.calc.er import Er
from src.usecase.ee_index.calc.euel import Euel
from src.usecase.ee_index.calc.h_component import HComponent
from src.usecase.ee_index.helper.params import CalcParams, Period


class EeFactory:
    def create_h(self, calc_params: CalcParams):
        return HComponent(calc_params)

    def create_er(self, calc_params: CalcParams):
        h = self.create_h(calc_params)
        return Er(h)

    def create_edst(self, period: Period):
        return Edst(period)

    def create_euel(self, calc_params: CalcParams):
        er = self.create_er(calc_params)
        edst = self.create_edst(calc_params.period)
        return Euel(er, edst)
