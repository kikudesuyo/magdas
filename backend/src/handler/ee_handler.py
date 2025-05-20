from datetime import timedelta
from typing import Iterable, List

import numpy as np
from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.usecase.ee_index.factory_ee import EeFactory
from src.utils.date import to_datetime


class EeIndexDateRangeReq(BaseModel):
    start_date: str
    days: int = Field(default=1, ge=1, le=30)  # Limit to 30 days maximum
    station_code: str

    @classmethod
    def from_query(
        cls,
        start_date: str = Query(alias="startDate", description="YYYY-MM-DD"),
        station_code: str = Query(alias="stationCode", description="station_code"),
        days: int = Query(
            alias="days",
            default=1,
            description="Number of days to fetch (1, 3, 7, or 30)",
        ),
    ):
        return cls(start_date=start_date, station_code=station_code, days=days)


def handle_get_ee_by_range(
    req: EeIndexDateRangeReq = Depends(EeIndexDateRangeReq.from_query),
):
    date, station_code, days = (
        req.start_date,
        req.station_code,
        req.days,
    )
    station = EeIndexStation[station_code]
    start_ut = to_datetime(date)

    period = Period(start_ut, start_ut + timedelta(days=days))
    params = StationParams(station=station, period=period)

    factory = EeFactory()
    er = factory.create_er(params)
    edst = factory.create_edst(period)
    euel = factory.create_euel(params)

    # for JSON serialization
    er_with_none = sanitize_np(er.calc_er())
    edst_with_none = sanitize_np(edst.calc_edst())
    euel_with_none = sanitize_np(euel.calc_euel())

    minute_labels = [
        (start_ut + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M")
        for i in range(days * 24 * 60)
    ]

    return JSONResponse(
        content={
            "values": {
                "er": er_with_none,
                "edst": edst_with_none,
                "euel": euel_with_none,
            },
            "minuteLabels": minute_labels,
        }
    )


def np_nan_to_none(values: np.ndarray) -> List[float | None]:
    return [None if np.isnan(x) else x for x in values]


def to_float(values: Iterable[float | None]) -> List[float | None]:
    return [float(x) if x is not None else None for x in values]


def sanitize_np(values: np.ndarray) -> List[float | None]:
    return to_float(np_nan_to_none(values))
