import numpy as np
from ee_index.src.plot.daily_ee_index_plotter import DailyEeIndexPlotter
from fastapi.responses import JSONResponse
from features.ee_index.types.ee_index import Ee_index
from utils.date import convert_datetime


def calc_daily_ee_index(request: Ee_index):
    date, station = request.date, request.station
    date = convert_datetime(date)
    plotter = DailyEeIndexPlotter(date)
    er, edst, euel = plotter.calculate_ee_values(station)
    er_with_none = [x if not np.isnan(x) else None for x in er]
    edst_with_none = [x if not np.isnan(x) else None for x in edst]
    euel_with_none = [x if not np.isnan(x) else None for x in euel]
    return JSONResponse(
        content={
            "values": {
                "er": er_with_none,
                "edst": edst_with_none,
                "euel": euel_with_none,
            }
        }
    )
