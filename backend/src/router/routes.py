from fastapi import APIRouter
from src.handler.calc_daily_ee_index import handle_calc_daily_ee_index
from src.handler.download_range_ee_index import handle_generate_ee_index_iaga_file

r = APIRouter()

r.add_api_route("/ee-index", handle_calc_daily_ee_index, methods=["POST"])
r.add_api_route(
    "/download/ee-index/daily", handle_generate_ee_index_iaga_file, methods=["POST"]
)
r.add_api_route(
    "/download/ee-index", handle_generate_ee_index_iaga_file, methods=["POST"]
)
