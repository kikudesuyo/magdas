from datetime import datetime

from src.domain.station_params import Period
from src.service.eej.brazil_eej_classification import BrazilClassificationPeculiarEej

lt_period = Period(datetime(2020, 1, 1, 0, 0), datetime(2020, 12, 31, 23, 59))
classification = BrazilClassificationPeculiarEej(lt_period)
classification.add_data()
