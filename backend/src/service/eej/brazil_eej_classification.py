from src.domain.magdas_station import EeIndexStation
from src.domain.region import Region
from src.domain.station_params import Period
from src.service.eej.peculiar_eej_classification import ClassificationPeculiarEej


class BrazilClassificationPeculiarEej:
    """ブラジル地域の特異型EEJの分類を行い,CSVに保存するクラス"""

    def __init__(self, lt_period: Period):
        self.lt_period = lt_period

    def add_data(self):
        classification = ClassificationPeculiarEej(
            lt_period=self.lt_period,
            dip_stations=[EeIndexStation.TTB],
            offdip_stations=[EeIndexStation.EUS, EeIndexStation.KOU],
            region=Region.BRAZIL,
        )
        classification.add_data()
