from fastapi import APIRouter
from src.handler.calc_daily_ee_index import handle_get_daily_ee_index
from src.handler.download_range_ee_index import handle_get_ee_index_iaga_file

r = APIRouter()

r.add_api_route("/ee-index", handle_get_daily_ee_index, methods=["GET"])
r.add_api_route(
    "/download/ee-index/daily", handle_get_ee_index_iaga_file, methods=["GET"]
)
r.add_api_route("/download/ee-index", handle_get_ee_index_iaga_file, methods=["GET"])
