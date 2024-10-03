import base64

import numpy as np
from ee_index.src.plot.daily_ee_index_plotter import DailyEeIndexPlotter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from features.downloads.iaga.meta_data import get_meta_data
from features.downloads.iaga.save_iaga_format import save_iaga_format
from features.downloads.zip.files_zipping import create_zip_buffer
from features.downloads.zip.remove_files import remove_files
from pydantic import BaseModel
from utils.date import convert_datetime
from utils.path import generate_abs_path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Ee_index(BaseModel):
    date: str
    station: str


@app.post("/ee-index")
async def ee_index(request: Ee_index):
    date, station = request.date, request.station
    date = convert_datetime(date)
    plotter = DailyEeIndexPlotter(date)
    er, edst, euel = plotter.calculate_ee_values(station)
    er_with_none = [x if not np.isnan(x) else None for x in er]
    edst_with_none = [x if not np.isnan(x) else None for x in edst]
    euel_with_none = [x if not np.isnan(x) else None for x in euel]
    return JSONResponse(
        content={
            "values": {
                "er": er_with_none,
                "edst": edst_with_none,
                "euel": euel_with_none,
            }
        }
    )


@app.post("/ee-index/download")
async def ee_index_download(request: Ee_index):
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
