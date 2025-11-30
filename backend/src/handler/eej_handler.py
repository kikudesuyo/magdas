from typing import List

from fastapi import Depends, Query
from pydantic import BaseModel, Field
from src.domain.region import Region
from src.usecase.eej import EejRow, EejUsecase
from src.utils.date import str_to_datetime


class EejReq(BaseModel):
    start_date: str
    days: int = Field(default=1, ge=1, le=30)  # Limit to 30 days maximum
    region: str

    @classmethod
    def from_query(
        cls,
        start_date: str = Query(alias="startDate", description="YYYY-MM-DD"),
        days: int = Query(
            alias="days",
            default=1,
            description="Number of days to fetch (1, 3, 7, or 30)",
        ),
        region: str = Query(alias="region", default="south_america"),
    ):
        return cls(start_date=start_date, days=days, region=region)


class EejResp(BaseModel):
    data: List[EejRow]
    peculiarEejDates: List[str]


def handle_get_eej_by_range(req: EejReq = Depends(EejReq.from_query)):
    start_lt = str_to_datetime(req.start_date)
    days = req.days
    region = Region.from_code(req.region)

    eej_usecase = EejUsecase(start_lt, days, region)
    eej_result = eej_usecase.execute()
    return EejResp(data=eej_result.data, peculiarEejDates=eej_result.peculiarEejDates)
