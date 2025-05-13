import base64
from datetime import timedelta

from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.constants.time_relation import Min, Sec
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.usecase.downloads.iaga_meta_data import get_meta_data
from src.usecase.downloads.iaga_save_file import save_iaga_format
from src.usecase.downloads.remove_files import remove_files
from src.usecase.downloads.zip_create import create_zip_buffer
from src.usecase.ee_index.calc_edst import Edst
from src.usecase.ee_index.calc_er import Er
from src.usecase.ee_index.calc_euel import Euel
from src.usecase.ee_index.calc_h_component import HComponent
from src.utils.date import to_datetime
from src.utils.path import generate_parent_abs_path


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
    dt = to_datetime(request.date)
    station = EeIndexStation[request.station_code]

    start_ut = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end_ut = dt.replace(hour=23, minute=59, second=59, microsecond=0)

    print(f"start_date: {start_ut}, end_date: {end_ut}, station_code: {station}")

    period = Period(start_ut, end_ut)
    params = StationParams(station, period)
    h = HComponent(params)
    er = Er(h)
    edst = Edst(period)
    euel = Euel(er, edst)
    er_values = er.calc_er()
    edst_values = edst.compute_smoothed_edst()
    euel_values = euel.calc_euel()

    # 修正するべき項目(IAGAコード、標高は未定)
    meta_data = get_meta_data(
        station,
        "",
        8888.88,
    )
    days = 1
    start_day_of_year = dt.timetuple().tm_yday
    data = {
        "DATE": [
            (dt + timedelta(days=j)).strftime("%Y-%m-%d")
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
    return JSONResponse(content={"file": zip_base64})
