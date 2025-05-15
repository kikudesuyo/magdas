from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.domain.magdas_station import EeIndexStation
from src.usecase.downloads.export_ee_index import export_ee_index_as_iaga
from src.utils.date import to_datetime


class DownloadEeIndexReq(BaseModel):
    start_date: str
    end_date: str
    station_code: str

    @classmethod
    def from_query(
        cls,
        start_date: str = Query(alias="startDate", description="YYYY-MM-DD"),
        end_date: str = Query(alias="endDate", description="YYYY-MM-DD"),
        station_code: str = Query(alias="stationCode", description="station_code"),
    ):
        return cls(start_date=start_date, end_date=end_date, station_code=station_code)


def handle_get_ee_index_zip_file(
    request: DownloadEeIndexReq = Depends(DownloadEeIndexReq.from_query),
):
    # TODO 現在のファイルははIAGA形式、もし他の形式を実装する場合は、クエリパラメータでフォーマットを指定させる
    start_date = request.start_date
    end_date = request.end_date
    station = EeIndexStation[request.station_code]
    start_ut = to_datetime(start_date).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    end_ut = to_datetime(end_date).replace(hour=23, minute=59, second=59, microsecond=0)

    zip_base64 = export_ee_index_as_iaga(station, start_ut, end_ut)
    return JSONResponse(content={"file": zip_base64})
