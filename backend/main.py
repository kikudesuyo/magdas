import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ee_index.src.plot.daily_ee_index_plotter import DailyEeIndexPlotter
from utils.date import convert_datetime

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
    dataKind: str
    station: str


@app.post("/ee-index")
async def ee_index(request: Ee_index):
    date, data_kind, station = request.date, request.dataKind, request.station
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
