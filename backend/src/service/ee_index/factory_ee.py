from src.domain.station_params import Period, StationParam
from src.service.ee_index.calc_edst import Edst
from src.service.ee_index.calc_er import Er
from src.service.ee_index.calc_euel import Euel
from src.service.ee_index.calc_h_component import HComponent


class EeFactory:
    def create_h(self, ut_params: StationParam):
        return HComponent(ut_params)

    def create_er(self, ut_params: StationParam):
        h = self.create_h(ut_params)
        return Er(h.get_equatorial_h())

    def create_edst(self, ut_period: Period):
        return Edst(ut_period)

    def create_euel(self, ut_params: StationParam):
        er = self.create_er(ut_params)
        edst = self.create_edst(ut_params.period)
        return Euel(er, edst)
