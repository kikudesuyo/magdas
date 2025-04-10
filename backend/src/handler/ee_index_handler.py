from datetime import timedelta

import numpy as np
from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.service.ee_index.calc.edst_index import Edst
from src.service.ee_index.calc.er_value import Er
from src.service.ee_index.calc.euel_index import Euel
from src.service.ee_index.constant.magdas_station import EeIndexStation
from src.service.ee_index.constant.time_relation import Day
from src.utils.date import convert_datetime


class DailyEeIndexReq(BaseModel):
    date: str
    station_code: str
    data_kind: str

    @classmethod
    def from_query(
        cls,
        date: str = Query(description="YYYY-MM-DD"),
        station_code: str = Query(alias="stationCode", description="station_code"),
        data_kind: str = Query(alias="dataKind", description="data_kind"),
    ):
        return cls(date=date, station_code=station_code, data_kind=data_kind)


def handle_get_daily_ee_index(
    req: DailyEeIndexReq = Depends(DailyEeIndexReq.from_query),
):
    date, station_code, data_kind = (
        req.date,
        req.station_code,
        req.data_kind,
    )
    print(f"date: {date}, station_code: {station_code}, data_kind: {data_kind}")
    station = EeIndexStation[station_code]
    start_ut = convert_datetime(date)
    end_ut = start_ut + timedelta(days=Day.ONE.const, minutes=-1)
    er = Er(station, start_ut, end_ut).calc_er()
    edst = Edst.compute_smoothed_edst(start_ut, end_ut)
    euel = Euel.calc_euel(station, start_ut, end_ut)
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
