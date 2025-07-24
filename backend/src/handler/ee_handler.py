from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from src.domain.magdas_station import EeIndexStation
from src.usecase.ee_by_days import EeIndexByDays
from src.utils.date import str_to_datetime


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
    start_ut = str_to_datetime(req.start_date)
    days = req.days
    station = EeIndexStation[req.station_code]

    ee_index = EeIndexByDays(start_ut, days, station)
    er, edst, euel = ee_index.get_ee_index()
    minute_labels = ee_index.get_minute_labels()

    return JSONResponse(
        content={
            "values": {
                "er": er,
                "edst": edst,
                "euel": euel,
            },
            "minuteLabels": minute_labels,
        }
    )
