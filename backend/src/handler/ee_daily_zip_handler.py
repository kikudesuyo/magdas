from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.domain.magdas_station import EeIndexStation
from src.usecase.downloads.export_ee_index import export_ee_index_as_iaga
from src.utils.date import to_datetime


class DownloadEeIndexReq(BaseModel):
    date: str
    station_code: str

    @classmethod
    def from_query(
        cls,
        date: str = Query(description="YYYY-MM-DD"),
        station_code: str = Query(alias="stationCode", description="station_code"),
    ):
        return cls(date=date, station_code=station_code)


def handle_get_daily_ee_index_zip_file(
    request: DownloadEeIndexReq = Depends(DownloadEeIndexReq.from_query),
):
    # TODO 現在のファイルははIAGA形式、もし他の形式を実装する場合は、クエリパラメータでフォーマットを指定させる
    ut = to_datetime(request.date)
    station = EeIndexStation[request.station_code]

    start_ut = ut.replace(hour=0, minute=0, second=0, microsecond=0)
    end_ut = ut.replace(hour=23, minute=59, second=59, microsecond=0)

    zip_base64 = export_ee_index_as_iaga(station, start_ut, end_ut)
    return JSONResponse(content={"file": zip_base64})
