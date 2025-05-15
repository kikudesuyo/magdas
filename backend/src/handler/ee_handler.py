from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from src.domain.magdas_station import EeIndexStation
from src.usecase.ee_index.ee_index_retrieval import get_ee_index_data
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


def handle_get_ee_index_by_date_range(
    req: EeIndexDateRangeReq = Depends(EeIndexDateRangeReq.from_query),
):
    date, station_code, days = (
        req.start_date,
        req.station_code,
        req.days,
    )
    station = EeIndexStation[station_code]
    start_ut = to_datetime(date)

    er_values, edst_values, euel_values, minute_labels = get_ee_index_data(
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
