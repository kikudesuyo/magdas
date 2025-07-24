from fastapi import Depends, Query
from pydantic import BaseModel
from src.domain.magdas_station import EeIndexStation
from src.usecase.ee_zip_by_range import EeIndexZipByRangeUsecase
from src.utils.date import str_to_datetime


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


class DownloadEeIndexResp(BaseModel):
    base64Zip: str
    fileName: str
    contentType: str


def handle_get_ee_zip_content_by_range(
    request: DownloadEeIndexReq = Depends(DownloadEeIndexReq.from_query),
) -> DownloadEeIndexResp:
    # TODO 現在のファイルははIAGA形式、もし他の形式を実装する場合は、クエリパラメータでフォーマットを指定させる
    start_date = str_to_datetime(request.start_date)
    end_date = str_to_datetime(request.end_date)
    station = EeIndexStation[request.station_code]

    ee_zip_usecase = EeIndexZipByRangeUsecase(start_date, end_date, station)
    zip_base64 = ee_zip_usecase.get_ee_as_iaga_zip()
    filename = ee_zip_usecase.get_filename()

    return DownloadEeIndexResp(
        base64Zip=zip_base64,
        fileName=filename,
        contentType="application/zip",
    )
