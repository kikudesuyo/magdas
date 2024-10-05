import base64
from datetime import timedelta

from ee_index.src.plot.custom_date_range_ee_index_plotter import CustomRangeEeIndex
from fastapi.responses import JSONResponse
from features.downloads.iaga.meta_data import get_meta_data
from features.downloads.iaga.save_iaga_format import save_iaga_format
from features.downloads.types.ee_index import RangeEeIndex
from features.downloads.zip.files_zipping import create_zip_buffer
from features.downloads.zip.remove_files import remove_files
from utils.date import convert_datetime
from utils.path import generate_abs_path


def calc_range_ee_index(request: RangeEeIndex):
    start_date, end_date, station = (
        request.startDate,
        request.endDate,
        request.station,
    )
    start_datetime, end_datetime = convert_datetime(start_date), convert_datetime(
        end_date
    )
    days = (end_datetime - start_datetime).days + 1
    plotter = CustomRangeEeIndex(start_datetime, end_datetime)
    er, edst, euel = plotter.calculate_ee_values(station)
    # 修正するべき項目(IAGAコード、標高は未定)
    meta_data = get_meta_data(station, "", "", "", 8888.88)
    start_day_of_year = start_datetime.timetuple().tm_yday
    data = {
        "DATE": [
            (start_datetime + timedelta(days=j)).strftime("%Y-%m-%d")
            for j in range(days)
            for _ in range(1440)
        ],
        "TIME": [
            f"{str((i % 1440) // 60).zfill(2)}:{str((i % 1440) % 60).zfill(2)}:00.000"
            for i in range(1440 * days)
        ],
        "DOY": [start_day_of_year + i for i in range(days) for _ in range(1440)],
        "EDst1h": edst,
        # 未作成
        "EDst6h": [0.0] * 1440 * days,
        "ER": er,
        "EUEL": euel,
    }
    save_iaga_format(meta_data, data, generate_abs_path("/tmp/iaga_format"))
    zip_buffer = create_zip_buffer()
    zip_base64 = base64.b64encode(zip_buffer.getvalue()).decode("utf-8")
    remove_files()
    return JSONResponse(content={"file": zip_base64})
