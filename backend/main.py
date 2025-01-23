from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from features.downloads.types.ee_index import RangeEeIndex
from features.ee_index.types.ee_index import DailyEeIndex
from handler.download.download_range_ee_index import generate_ee_index_iaga_file
from handler.ee_index.calc_daily_ee_index import (
    calc_daily_ee_index as handle_calc_daily_ee_index,
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/ee-index")
async def calc_daily_ee_index(request: DailyEeIndex):
    return handle_calc_daily_ee_index(request)


@app.post("/download/ee-index/daily")
async def download_daily_ee_index(request: DailyEeIndex):
    r = RangeEeIndex(
        startDate=request.date,
        endDate=request.date,
        station=request.station,
    )
    return generate_ee_index_iaga_file(r)


@app.post("/download/ee-index")
async def download_ee_index(request: RangeEeIndex):
    return generate_ee_index_iaga_file(request)
