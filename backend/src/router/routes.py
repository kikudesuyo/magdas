from fastapi import APIRouter

from backend.src.handler.ee_index_handler import handle_get_daily_ee_index
from backend.src.handler.ee_index_zip_handler import handle_get_ee_index_zip_file

r = APIRouter()

r.add_api_route("/ee-index", handle_get_daily_ee_index, methods=["GET"])
r.add_api_route(
    "/download/ee-index/daily", handle_get_ee_index_zip_file, methods=["GET"]
)
r.add_api_route("/download/ee-index", handle_get_ee_index_zip_file, methods=["GET"])
