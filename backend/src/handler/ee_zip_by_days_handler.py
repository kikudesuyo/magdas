from fastapi import Depends, Query
from pydantic import BaseModel, Field
from src.domain.magdas_station import EeIndexStation
from src.usecase.ee_zip import EeIndexZipUsecase
from src.utils.date import str_to_datetime


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


class DownloadEeIndexResp(BaseModel):
    base64Zip: str
    fileName: str
    contentType: str


def handle_get_ee_zip_content_by_days(
    request: DownloadEeIndexReq = Depends(DownloadEeIndexReq.from_query),
) -> DownloadEeIndexResp:
    # TODO 現在のファイルははIAGA形式、もし他の形式を実装する場合は、クエリパラメータでフォーマットを指定させる
    station = EeIndexStation[request.station_code]
    date = str_to_datetime(request.start_date)

    ee_zip_usecase = EeIndexZipUsecase(station)
    ee_zip_data = ee_zip_usecase.get_ee_zip_by_days(date, request.days)

    return DownloadEeIndexResp(
        base64Zip=ee_zip_data.zip_base64,
        fileName=ee_zip_data.filename,
        contentType="application/zip",
    )
