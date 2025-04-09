from datetime import timedelta

import numpy as np
from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.service.ee_index.calc.edst_index import Edst
from src.service.ee_index.calc.er_value import Er
from src.service.ee_index.calc.euel_index import Euel
from src.service.ee_index.constant.time_relation import Day
from src.utils.date import convert_datetime


class DailyEeIndexReq(BaseModel):
    date: str
    station: str
    data_kind: str

    @classmethod
    def from_query(
        cls,
        date: str = Query(description="YYYY-MM-DD"),
        station: str = Query(description="station"),
        data_kind: str = Query(alias="dataKind", description="data_kind"),
    ):
        return cls(date=date, station=station, data_kind=data_kind)


def handle_get_daily_ee_index(
    req: DailyEeIndexReq = Depends(DailyEeIndexReq.from_query),
):
    date, station, data_kind = (
        req.date,
        req.station,
        req.data_kind,
    )
    start_dt = convert_datetime(date)
    end_dt = start_dt + timedelta(days=Day.ONE.const, minutes=-1)
    er = Er(station, start_dt, end_dt).calc_er()
    edst = Edst.compute_smoothed_edst(start_dt, end_dt)
    euel = Euel.calc_euel(station, start_dt, end_dt)
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
