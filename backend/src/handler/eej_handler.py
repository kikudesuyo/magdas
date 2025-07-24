from typing import List, Optional

from fastapi import Depends, Query
from pydantic import BaseModel, Field
from src.domain.region import Region
from src.usecase.eej import EejUsecase
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


class EejRow(BaseModel):
    time: str
    dip_euel: Optional[float] = Field(alias="dipEuel")
    offdip_euel: Optional[float] = Field(alias="offdipEuel")


class EejResp(BaseModel):
    data: List[EejRow]
    peculiarEejDates: List[str]


def handle_get_eej_by_range(req: EejReq = Depends(EejReq.from_query)):
    start_lt = str_to_datetime(req.start_date)
    days = req.days
    region = Region.from_code(req.region)

    if region.code != "south_america":
        raise ValueError("Only 'south_america' region is supported for EEJ detection.")

    eejUsecase = EejUsecase(start_lt, days, region)
    peculiar_eej_dates = eejUsecase.get_peculiar_eej_dates()
    minute_labels = eejUsecase.get_minute_labels()
    dip_euel, offdip_euel = eejUsecase.get_local_euel()

    return EejResp(
        data=[
            EejRow(
                time=minute_labels[i],
                dipEuel=dip_euel[i],
                offdipEuel=offdip_euel[i],
            )
            for i in range(len(minute_labels))
        ],
        peculiarEejDates=[date.strftime("%Y-%m-%d") for date in peculiar_eej_dates],
    )
