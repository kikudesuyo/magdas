import base64

from ee_index.src.plot.daily_ee_index_plotter import DailyEeIndexPlotter
from fastapi.responses import JSONResponse
from features.ee_index.downloads.iaga.meta_data import get_meta_data
from features.ee_index.downloads.iaga.save_iaga_format import save_iaga_format
from features.ee_index.downloads.zip.files_zipping import create_zip_buffer
from features.ee_index.downloads.zip.remove_files import remove_files
from features.ee_index.types.ee_index import Ee_index
from utils.date import convert_datetime
from utils.path import generate_abs_path


def ee_index_download(request: Ee_index):
    date, station = request.date, request.station
    plotter = DailyEeIndexPlotter(convert_datetime(date))
    er, edst, euel = plotter.calculate_ee_values(station)
    # 修正するべき項目(IAGAコード、標高は未定)
    meta_data = get_meta_data(station, "", -12.000, 284.710, 8888.88)
    data = {
        "DATE": [date] * 1440,
        "TIME": [
            f"{str(i//60).zfill(2)}:{str(i%60).zfill(2)}:00.000" for i in range(1440)
        ],
        "DOY": [78] * 1440,
        "EDst1h": edst,
        "EDst6h": edst,
        "ER": er,
        "EUEL": euel,
    }
    save_iaga_format(meta_data, data, generate_abs_path("/tmp/iaga_format"))
    zip_buffer = create_zip_buffer()
    zip_base64 = base64.b64encode(zip_buffer.getvalue()).decode("utf-8")
    remove_files()
    return JSONResponse(content={"file": zip_base64})
