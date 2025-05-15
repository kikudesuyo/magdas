from datetime import timedelta

from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from src.domain.magdas_station import EeIndexStation
from src.usecase.downloads.export_ee_index import export_ee_index_as_iaga
from src.utils.date import to_datetime


class DownloadEeIndexReq(BaseModel):
    start_date: str
    days: int = Field(default=1, ge=1, le=365)
    station_code: str

    @classmethod
    def from_query(
        cls,
        start_date: str = Query(alias="startDate", description="YYYY-MM-DD"),
        days: int = Query(
            default=1, description="Number of days to fetch (1, 3, 7, or 30)"
        ),
        station_code: str = Query(alias="stationCode", description="station_code"),
    ):
        return cls(start_date=start_date, days=days, station_code=station_code)


def handle_get_ee_index_zip_file_by_days(
    request: DownloadEeIndexReq = Depends(DownloadEeIndexReq.from_query),
):
    # TODO 現在のファイルははIAGA形式、もし他の形式を実装する場合は、クエリパラメータでフォーマットを指定させる
    station = EeIndexStation[request.station_code]
    start_dt = to_datetime(request.start_date)

    start_ut = start_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end_ut = start_ut.replace(hour=23, minute=59, second=59, microsecond=0) + timedelta(
        days=request.days - 1
    )

    zip_base64 = export_ee_index_as_iaga(station, start_ut, end_ut)

    start_date = start_ut.strftime("%Y-%m-%d")
    end_date = end_ut.strftime("%Y-%m-%d")
    return JSONResponse(
        content={
            "base64Zip": zip_base64,
            "fileName": f"ee_index_{start_date}_to_{end_date}.zip",
            "contentType": "application/zip",
        }
    )
