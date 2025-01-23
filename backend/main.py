from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from features.downloads.types.ee_index import RangeEeIndex
from features.ee_index.types.ee_index import Ee_index
from handler.download.download_range_ee_index import (
    calc_range_ee_index as handle_calc_range_ee_index,
)
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
async def calc_daily_ee_index(request: Ee_index):
    return handle_calc_daily_ee_index(request)


@app.post("/download/ee-index")
async def download_ee_index(request: RangeEeIndex):
    return handle_calc_range_ee_index(request)
