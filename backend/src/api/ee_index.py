from fastapi import APIRouter
from src.features.downloads.types.ee_index import RangeEeIndex
from src.features.ee_index.types.ee_index import DailyEeIndex
from src.handler.calc_daily_ee_index import handle_calc_daily_ee_index
from src.handler.download_range_ee_index import handle_generate_ee_index_iaga_file

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
    return handle_generate_ee_index_iaga_file(r)


@router.post("/download/ee-index")
async def download_ee_index(request: RangeEeIndex):
    return handle_generate_ee_index_iaga_file(request)
