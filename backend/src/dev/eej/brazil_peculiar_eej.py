from datetime import datetime

from src.domain.station_params import Period
from src.service.eej.brazil_eej_classification import BrazilClassificationPeculiarEej

if __name__ == "__main__":
    lt_period = Period(datetime(2008, 1, 1, 0, 0), datetime(2014, 12, 31, 23, 59))
    classification = BrazilClassificationPeculiarEej(lt_period)
    classification.add_data()
