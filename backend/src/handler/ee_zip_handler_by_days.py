import base64
from datetime import timedelta

from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from src.constants.time_relation import Min, Sec
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.usecase.downloads.iaga_meta_data import get_meta_data
from src.usecase.downloads.iaga_save_file import save_iaga_format
from src.usecase.downloads.remove_files import remove_files
from src.usecase.downloads.zip_create import create_zip_buffer
from src.usecase.ee_index.factory_ee import EeFactory
from src.utils.date import to_datetime
from src.utils.path import generate_parent_abs_path


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
    start_dt = to_datetime(request.start_date)

    start_ut = start_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end_ut = start_ut.replace(hour=23, minute=59, second=59, microsecond=0) + timedelta(
        days=request.days - 1
    )
    days = request.days
    station = EeIndexStation[request.station_code]

    period = Period(start_ut, end_ut)
    params = StationParams(station, period)

    factory = EeFactory()
    er = factory.create_er(params)
    edst = factory.create_edst(period)
    euel = factory.create_euel(params)

    er_values = er.calc_er()
    edst_values = edst.compute_smoothed_edst()
    euel_values = euel.calc_euel()

    # 修正するべき項目(IAGAコード、標高は未定)
    meta_data = get_meta_data(
        station,
        "",
        8888.88,
    )
    start_day_of_year = start_ut.timetuple().tm_yday
    data = {
        "DATE": [
            (start_ut + timedelta(days=j)).strftime("%Y-%m-%d")
            for j in range(days)
            for _ in range(Min.ONE_DAY.const)
        ],
        "TIME": [
            f"{str((i % Min.ONE_DAY.const) // Min.ONE_HOUR.const).zfill(2)}:{str((i % Min.ONE_DAY.const) % Sec.ONE_MINUTE.const).zfill(2)}:00.000"
            for i in range(Min.ONE_DAY.const * days)
        ],
        "DOY": [
            start_day_of_year + i for i in range(days) for _ in range(Min.ONE_DAY.const)
        ],
        "EDst1h": edst_values,
        # 未作成
        "EDst6h": [0.0] * Min.ONE_DAY.const * days,
        "ER": er_values,
        "EUEL": euel_values,
    }
    save_iaga_format(meta_data, data, generate_parent_abs_path("/tmp/iaga_format.txt"))
    zip_buffer = create_zip_buffer()
    zip_base64 = base64.b64encode(zip_buffer.getvalue()).decode("utf-8")
    remove_files()

    start_date = start_ut.strftime("%Y-%m-%d")
    end_date = end_ut.strftime("%Y-%m-%d")
    return JSONResponse(
        content={
            "base64Zip": zip_base64,
            "fileName": f"ee_index_{start_date}_to_{end_date}.zip",
            "contentType": "application/zip",
        }
    )
