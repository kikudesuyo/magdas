import base64
from datetime import timedelta

from fastapi.responses import JSONResponse
from src.ee_index.calc.edst_index import Edst
from src.ee_index.calc.er_value import Er
from src.ee_index.calc.euel_index import Euel
from src.ee_index.constant.magdas_station import EeIndexStation
from src.ee_index.constant.time_relation import Min, Sec
from src.handler.types.ee_index import RangeEeIndex
from src.service.downloads.iaga.meta_data import get_meta_data
from src.service.downloads.iaga.save_iaga_format import save_iaga_format
from src.service.downloads.zip.files_zipping import create_zip_buffer
from src.service.downloads.zip.remove_files import remove_files
from src.utils.date import convert_datetime
from src.utils.path import generate_abs_path


def handle_generate_ee_index_iaga_file(request: RangeEeIndex):
    start_date, end_date, station = (
        request.startDate,
        request.endDate,
        request.station,
    )
    start_date, end_date = convert_datetime(start_date), convert_datetime(end_date)
    start_dt = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_dt = end_date.replace(hour=23, minute=59, second=59, microsecond=0)
    er = Er(station, start_dt, end_dt).calc_er()
    edst = Edst.compute_smoothed_edst(start_dt, end_dt)
    euel = Euel.calc_euel(station, start_dt, end_dt)
    # 修正するべき項目(IAGAコード、標高は未定)
    meta_data = get_meta_data(
        station,
        "",
        EeIndexStation[station].gm_lat,
        EeIndexStation[station].gm_lon,
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
