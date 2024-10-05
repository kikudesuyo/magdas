import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from handler.ee_index.calc_daily_ee_index import Ee_index
from handler.ee_index.calc_daily_ee_index import (
    calc_daily_ee_index as handle_calc_daily_ee_index,
)
from handler.ee_index.download_daily_ee_index import (
    ee_index_download as handle_ee_index_download,
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


@app.post("/ee-index/download")
async def ee_index_download(request: Ee_index):
    hoge = handle_ee_index_download(request)
    time.sleep(10)
    return hoge
