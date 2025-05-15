from datetime import timedelta

import numpy as np
from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.constants.time_relation import Day
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.usecase.ee_index.calc_edst import Edst
from src.usecase.ee_index.calc_er import Er
from src.usecase.ee_index.calc_euel import Euel
from src.usecase.ee_index.calc_h_component import HComponent
from src.utils.date import to_datetime


class DailyEeIndexReq(BaseModel):
    date: str
    station_code: str

    @classmethod
    def from_query(
        cls,
        date: str = Query(description="YYYY-MM-DD"),
        station_code: str = Query(alias="stationCode", description="station_code"),
    ):
        return cls(date=date, station_code=station_code)


def handle_get_daily_ee_index(
    req: DailyEeIndexReq = Depends(DailyEeIndexReq.from_query),
):
    date, station_code = (
        req.date,
        req.station_code,
    )
    print(f"date: {date}, station_code: {station_code}")
    station = EeIndexStation[station_code]
    start_ut = to_datetime(date)
    end_ut = start_ut + timedelta(days=Day.ONE.const, minutes=-1)

    period = Period(start_ut, end_ut)
    params = StationParams(station=station, period=period)
    h = HComponent(params)
    er = Er(h)
    edst = Edst(period)
    euel = Euel(er, edst)
    er_values = er.calc_er()
    edst_values = edst.compute_smoothed_edst()
    euel_values = euel.calc_euel()
    er_with_none = [float(x) if not np.isnan(x) else None for x in er_values]
    edst_with_none = [float(x) if not np.isnan(x) else None for x in edst_values]
    euel_with_none = [float(x) if not np.isnan(x) else None for x in euel_values]
    return JSONResponse(
        content={
            "values": {
                "er": er_with_none,
                "edst": edst_with_none,
                "euel": euel_with_none,
            }
        }
    )
