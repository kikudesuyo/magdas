from datetime import datetime

from src.domain.station_params import Period
from src.service.eej.south_america_eej_classification import (
    SouthAmericaClassificationPeculiarEej,
)

lt_period = Period(datetime(2008, 1, 1, 0, 0), datetime(2008, 1, 31, 23, 59))
classification = SouthAmericaClassificationPeculiarEej(lt_period)
classification.add_data()
