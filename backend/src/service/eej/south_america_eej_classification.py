from datetime import datetime

from src.domain.magdas_station import EeIndexStation
from src.domain.region import Region
from src.domain.station_params import Period
from src.service.eej.peculiar_eej_classification import ClassificationPeculiarEej


class SouthAmericaClassificationPeculiarEej:
    """南アメリカ地域の特異型EEJの分類を行い,CSVに保存するクラス"""

    def __init__(self, lt_period: Period):
        self.lt_period = lt_period

    def create(self):
        return ClassificationPeculiarEej(
            lt_period=self.lt_period,
            dip_stations=[EeIndexStation.TTB, EeIndexStation.KOU],
            offdip_stations=[EeIndexStation.EUS],
            region=Region.BRAZIL,
        )

    def save(self):
        classification = self.create()
        classification.add_data()


# 実行例
if __name__ == "__main__":
    lt_period = Period(datetime(2008, 1, 1, 0, 0), datetime(2008, 1, 31, 23, 59))
    classification = SouthAmericaClassificationPeculiarEej(lt_period)
    classification.save()
