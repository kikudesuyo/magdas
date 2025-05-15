from datetime import datetime, timedelta
from typing import List, Optional

import numpy as np
from fastapi import Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from src.constants.time_relation import Day
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.usecase.ee_index.calc_edst import Edst
from src.usecase.ee_index.calc_er import Er
from src.usecase.ee_index.calc_euel import Euel
from src.usecase.ee_index.calc_h_component import HComponent
from src.utils.date import to_datetime


class DailyEeIndexReq(BaseModel):
    date: str
    station_code: str
    days: int = Field(default=1, ge=1, le=30)  # Limit to 30 days maximum

    @classmethod
    def from_query(
        cls,
        date: str = Query(description="YYYY-MM-DD"),
        station_code: str = Query(alias="stationCode", description="station_code"),
        days: Optional[int] = Query(default=1, description="Number of days to fetch (1, 3, 7, or 30)"),
    ):
        # Validate days parameter
        valid_days = [1, 3, 7, 30]
        if days not in valid_days:
            days = 1  # Default to 1 day if invalid
        
        return cls(date=date, station_code=station_code, days=days)


def fetch_data_for_period(station: EeIndexStation, start_date: datetime, days: int) -> tuple[List[float], List[float], List[float], List[str]]:
    """Fetch data for a specific period and return combined values."""
    all_er_values = []
    all_edst_values = []
    all_euel_values = []
    date_strings = []
    
    for day_offset in range(days):
        current_date = start_date + timedelta(days=day_offset)
        end_date = current_date + timedelta(days=Day.ONE.const, minutes=-1)
        
        # Format date for response
        date_str = current_date.strftime("%Y-%m-%d")
        date_strings.append(date_str)
        
        period = Period(current_date, end_date)
        params = StationParams(station=station, period=period)
        
        # Calculate values for this day
        h = HComponent(params)
        er = Er(h)
        edst = Edst(period)
        euel = Euel(er, edst)
        
        er_values = er.calc_er()
        edst_values = edst.compute_smoothed_edst()
        euel_values = euel.calc_euel()
        
        # Convert NaN to None for JSON serialization
        er_with_none = [float(x) if not np.isnan(x) else None for x in er_values]
        edst_with_none = [float(x) if not np.isnan(x) else None for x in edst_values]
        euel_with_none = [float(x) if not np.isnan(x) else None for x in euel_values]
        
        # Add to combined arrays
        all_er_values.extend(er_with_none)
        all_edst_values.extend(edst_with_none)
        all_euel_values.extend(euel_with_none)
    
    return all_er_values, all_edst_values, all_euel_values, date_strings


def handle_get_daily_ee_index(
    req: DailyEeIndexReq = Depends(DailyEeIndexReq.from_query),
):
    date, station_code, days = (
        req.date,
        req.station_code,
        req.days,
    )
    print(f"date: {date}, station_code: {station_code}, days: {days}")
    
    station = EeIndexStation[station_code]
    start_ut = to_datetime(date)
    
    # Fetch data for the requested period
    er_values, edst_values, euel_values, date_strings = fetch_data_for_period(
        station, start_ut, days
    )
    
    return JSONResponse(
        content={
            "values": {
                "er": er_values,
                "edst": edst_values,
                "euel": euel_values,
            },
            "dates": date_strings
        }
    )
