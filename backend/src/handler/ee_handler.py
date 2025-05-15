from datetime import datetime, timedelta
from typing import List, Optional

import numpy as np
from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.usecase.ee_index.factory_ee import EeFactory
from src.utils.date import to_datetime


class DailyEeIndexReq(BaseModel):
    start_date: str
    station_code: str
    days: int = Field(default=1, ge=1, le=30)  # Limit to 30 days maximum

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


def handle_get_daily_ee_index(
    req: DailyEeIndexReq = Depends(DailyEeIndexReq.from_query),
):
    date, station_code, days = (
        req.start_date,
        req.station_code,
        req.days,
    )
    station = EeIndexStation[station_code]
    start_ut = to_datetime(date)

    # Fetch data for the requested period
    er_values, edst_values, euel_values, minute_labels = fetch_data_for_period(
        station, start_ut, days
    )

    return JSONResponse(
        content={
            "values": {
                "er": er_values,
                "edst": edst_values,
                "euel": euel_values,
            },
            "minuteLabels": minute_labels,
        }
    )


def fetch_data_for_period(
    station: EeIndexStation, start_ut: datetime, days: int
) -> tuple[
    List[Optional[float]], List[Optional[float]], List[Optional[float]], List[str]
]:
    """Fetch data for a specific period and return combined values."""

    period = Period(start_ut, start_ut + timedelta(days=days))
    params = StationParams(station=station, period=period)

    factory = EeFactory()
    er = factory.create_er(params)
    edst = factory.create_edst(period)
    euel = factory.create_euel(params)

    er_values = er.calc_er()
    edst_values = edst.compute_smoothed_edst()
    euel_values = euel.calc_euel()

    # Convert NaN to None for JSON serialization
    er_with_none = [float(x) if not np.isnan(x) else None for x in er_values]
    edst_with_none = [float(x) if not np.isnan(x) else None for x in edst_values]
    euel_with_none = [float(x) if not np.isnan(x) else None for x in euel_values]

    minute_labels = [
        (start_ut + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M")
        for i in range(days * 24 * 60)
    ]

    return (
        er_with_none,
        edst_with_none,
        euel_with_none,
        minute_labels,
    )
