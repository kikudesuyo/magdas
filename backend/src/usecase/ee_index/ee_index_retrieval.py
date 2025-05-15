from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import numpy as np
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.usecase.ee_index.factory_ee import EeFactory


def get_ee_index_data(
    station: EeIndexStation, start_ut: datetime, days: int
) -> Tuple[
    List[Optional[float]], List[Optional[float]], List[Optional[float]], List[str]
]:
    """
    Retrieve EE index data for a specific period.
    
    Args:
        station: The station to get data for
        start_ut: Start datetime
        days: Number of days to fetch
        
    Returns:
        Tuple containing ER values, EDst values, EUEL values, and minute labels
    """
    period = Period(start_ut, start_ut + timedelta(days=days))
    params = StationParams(station=station, period=period)

    factory = EeFactory()
    er = factory.create_er(params)
    edst = factory.create_edst(period)
    euel = factory.create_euel(params)

    er_values = er.calc_er()
    edst_values = edst.compute_smoothed_edst()
    euel_values = euel.calc_euel()

    # Convert NaN to None for JSON serialization
    er_with_none = [float(x) if not np.isnan(x) else None for x in er_values]
    edst_with_none = [float(x) if not np.isnan(x) else None for x in edst_values]
    euel_with_none = [float(x) if not np.isnan(x) else None for x in euel_values]

    minute_labels = [
        (start_ut + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M")
        for i in range(days * 24 * 60)
    ]

    return (
        er_with_none,
        edst_with_none,
        euel_with_none,
        minute_labels,
    )