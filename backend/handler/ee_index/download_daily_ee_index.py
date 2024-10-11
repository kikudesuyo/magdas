import base64

from ee_index.src.calc.edst_index import Edst
from ee_index.src.calc.er_value import Er
from ee_index.src.calc.euel_index import Euel
from ee_index.src.constant.magdas_station import EeIndexStation
from ee_index.src.constant.time_relation import Day, Min, Sec
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
    date = convert_datetime(date)
    er = Er(station, date).calc_er_for_days(Day.ONE.const)
    edst = Edst.compute_smoothed_edst(date, Day.ONE.const)
    euel = Euel.calculate_euel_for_days(
        station,
        date,
        Day.ONE.const,
    )
    # 修正するべき項目(IAGAコード、標高は未定)
    meta_data = get_meta_data(
        station,
        "",
        EeIndexStation[station].gm_lat,
        EeIndexStation[station].gm_lon,
        8888.88,
    )
    data = {
        "DATE": [date] * Min.ONE_DAY.const,
        "TIME": [
            f"{str(i//Min.ONE_HOUR.const).zfill(2)}:{str(i%Sec.ONE_MINUTE.const).zfill(2)}:00.000"
            for i in range(Min.ONE_DAY.const)
        ],
        "DOY": [78] * Min.ONE_DAY.const,
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
