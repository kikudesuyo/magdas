import base64
from datetime import timedelta

from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.service.downloads.iaga_meta_data import get_meta_data
from src.service.downloads.iaga_save_file import save_iaga_format
from src.service.downloads.remove_files import remove_files
from src.service.downloads.zip_create import create_zip_buffer
from src.service.ee_index.calc.edst_index import Edst
from src.service.ee_index.calc.er_value import Er
from src.service.ee_index.calc.euel_index import Euel
from src.service.ee_index.constant.magdas_station import EeIndexStation
from src.service.ee_index.constant.time_relation import Min, Sec
from src.utils.date import convert_datetime
from src.utils.path import generate_abs_path


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
    start_date, end_date, station = (
        request.start_date,
        request.end_date,
        request.station_code,
    )
    station = EeIndexStation[station]
    start_date, end_date = convert_datetime(start_date), convert_datetime(end_date)
    start_ut = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_ut = end_date.replace(hour=23, minute=59, second=59, microsecond=0)
    er = Er(station, start_ut, end_ut).calc_er()
    edst = Edst.compute_smoothed_edst(start_ut, end_ut)
    euel = Euel.calc_euel(station, start_ut, end_ut)
    # 修正するべき項目(IAGAコード、標高は未定)
    meta_data = get_meta_data(
        station,
        "",
        8888.88,
    )
    days = (end_date - start_date).days + 1
    start_day_of_year = start_date.timetuple().tm_yday
    data = {
        "DATE": [
            (start_date + timedelta(days=j)).strftime("%Y-%m-%d")
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
        "EDst1h": edst,
        # 未作成
        "EDst6h": [0.0] * Min.ONE_DAY.const * days,
        "ER": er,
        "EUEL": euel,
    }
    save_iaga_format(meta_data, data, generate_abs_path("/tmp/iaga_format.txt"))
    zip_buffer = create_zip_buffer()
    zip_base64 = base64.b64encode(zip_buffer.getvalue()).decode("utf-8")
    remove_files()
    return JSONResponse(content={"file": zip_base64})
