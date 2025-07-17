from datetime import timedelta
from typing import Iterable, List, Optional

import numpy as np
from fastapi import Depends, Query
from pydantic import BaseModel, Field
from src.constants.time_relation import TimeUnit
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.service.ee_index.calc_eej_detection import (
    BestEuelSelectorForEej,
    EejDetection,
    calc_euel_peak_diff,
)
from src.service.ee_index.factory_ee import EeFactory
from src.service.nan_calculator import NanCalculator
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
        region: str = Query(
            alias="region",
            default="south-america",
        ),
    ):
        return cls(
            start_date=start_date,
            days=days,
            region=region,
        )


class EejRow(BaseModel):
    time: str
    dip_euel: Optional[float] = Field(alias="dipEuel")
    offdip_euel: Optional[float] = Field(alias="offdipEuel")


class EejResp(BaseModel):
    data: List[EejRow]
    peculiarEejDates: List[str]


def handle_get_eej_by_range(
    req: EejReq = Depends(EejReq.from_query),
):
    str_date, days, region = (req.start_date, req.days, req.region)
    start_lt = str_to_datetime(str_date)

    if region != "south-america":
        raise ValueError("Only 'south_america' region is supported for EEJ detection.")
    dip_stations = [
        EeIndexStation.ANC,
        EeIndexStation.HUA,
    ]
    offdip_stations = [EeIndexStation.EUS]

    factory = EeFactory()
    anc_param = StationParams(
        EeIndexStation.ANC, Period(start_lt, start_lt + timedelta(days=days))
    ).to_ut_params()
    anc_euel = factory.create_euel(anc_param).calc_euel()
    hua_param = StationParams(
        EeIndexStation.HUA, Period(start_lt, start_lt + timedelta(days=days))
    ).to_ut_params()
    hua_euel = factory.create_euel(hua_param).calc_euel()

    dip_euel = sanitize_np(
        NanCalculator.nanmean(np.array([anc_euel, hua_euel]), axis=0)
    )

    eus_param = StationParams(
        EeIndexStation.EUS, Period(start_lt, start_lt + timedelta(days=days))
    ).to_ut_params()
    offdip_euel = sanitize_np(factory.create_euel(eus_param).calc_euel())

    peculiar_eej_dates = []
    current_lt = start_lt
    for i in range(days):
        current_lt += timedelta(days=i)
        dip_euel_selector = BestEuelSelectorForEej(
            dip_stations, current_lt, is_dip=True
        )
        offdip_euel_selector = BestEuelSelectorForEej(
            offdip_stations, current_lt, is_dip=False
        )

        dip_euel_data = dip_euel_selector.select_euel_data()
        offdip_euel_data = offdip_euel_selector.select_euel_data()

        peak_diff = calc_euel_peak_diff(
            dip_euel_data,
            offdip_euel_data,
            current_lt,
        )

        eej_detection = EejDetection(peak_diff, current_lt)
        if eej_detection.is_peculiar_eej():
            peculiar_eej_dates.append(current_lt.date())

    minute_labels = [
        (start_lt + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M")
        for i in range(days * TimeUnit.ONE_DAY.min)
    ]

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


def np_nan_to_none(values: np.ndarray) -> List[float | None]:
    return [None if np.isnan(x) else x for x in values]


def to_float(values: Iterable[float | None]) -> List[float | None]:
    return [float(x) if x is not None else None for x in values]


def sanitize_np(values: np.ndarray) -> List[float | None]:
    return to_float(np_nan_to_none(values))
