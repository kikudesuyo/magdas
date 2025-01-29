import numpy as np
from fastapi.responses import JSONResponse
from src.ee_index.calc.edst_index import Edst
from src.ee_index.calc.er_value import Er
from src.ee_index.calc.euel_index import Euel
from src.ee_index.constant.time_relation import Day
from src.features.types.ee_index import DailyEeIndex
from src.utils.date import convert_datetime


def handle_calc_daily_ee_index(request: DailyEeIndex):
    date, station = request.date, request.station
    date = convert_datetime(date)
    er = Er(station, date).calc_er_for_days(Day.ONE.const)
    edst = Edst.compute_smoothed_edst(date, Day.ONE.const)
    euel = Euel.calculate_euel_for_days(
        station,
        date,
        Day.ONE.const,
    )
    er_with_none = [float(x) if not np.isnan(x) else None for x in er]
    edst_with_none = [float(x) if not np.isnan(x) else None for x in edst]
    euel_with_none = [float(x) if not np.isnan(x) else None for x in euel]
    return JSONResponse(
        content={
            "values": {
                "er": er_with_none,
                "edst": edst_with_none,
                "euel": euel_with_none,
            }
        }
    )
