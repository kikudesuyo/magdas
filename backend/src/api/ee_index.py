from fastapi import APIRouter
from src.features.downloads.types.ee_index import RangeEeIndex
from src.features.ee_index.types.ee_index import DailyEeIndex
from src.handler.download.download_range_ee_index import generate_ee_index_iaga_file
from src.handler.ee_index.calc_daily_ee_index import (
    calc_daily_ee_index as handle_calc_daily_ee_index,
)

router = APIRouter()


@router.post("/ee-index")
async def calc_daily_ee_index(request: DailyEeIndex):
    return handle_calc_daily_ee_index(request)


@router.post("/download/ee-index/daily")
async def download_daily_ee_index(request: DailyEeIndex):
    r = RangeEeIndex(
        startDate=request.date,
        endDate=request.date,
        station=request.station,
    )
    return generate_ee_index_iaga_file(r)


@router.post("/download/ee-index")
async def download_ee_index(request: RangeEeIndex):
    return generate_ee_index_iaga_file(request)
