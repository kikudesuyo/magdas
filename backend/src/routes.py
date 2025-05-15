from fastapi import APIRouter
from src.handler.ee_handler import handle_get_ee_index_by_date_range
from src.handler.ee_zip_handler_by_days import handle_get_ee_index_zip_file_by_days
from src.handler.ee_zip_handler_by_range import handle_get_ee_index_zip_file_by_range

r = APIRouter()


r.add_api_route("/ee-index", handle_get_ee_index_by_date_range, methods=["GET"])
r.add_api_route(
    "/download/ee-index/by-days", handle_get_ee_index_zip_file_by_days, methods=["GET"]
)
r.add_api_route(
    "/download/ee-index/by-range",
    handle_get_ee_index_zip_file_by_range,
    methods=["GET"],
)
