from dataclasses import dataclass
from enum import Enum


@dataclass
class MagdasStation:
    code: str
    time_diff: float
    gm_lat: float
    gm_lon: float


class EeIndexStation(Enum):
    """
    Ref: https://data.i-spes.kyushu-u.ac.jp/eeindex/SG_v11_No1_2016-pp-37-47.pdf
    """

    # 藤本論文2015での観測点データ
    AAB = MagdasStation("AAB", 2.585333333333333, 0.18, 110.47)
    ABU = MagdasStation("ABU", 0.49266666666666664, -1.53, 79.4)
    AMA = MagdasStation("AMA", 8.622, 21.11, 200.88)
    ANC = MagdasStation("ANC", -5.143333333333333, 0.77, 354.33)
    BCL = MagdasStation("BCL", 7.047333333333333, -0.66, 177.96)
    BKL = MagdasStation("BKL", 6.820666666666667, -15.13, 173.6)
    CDO = MagdasStation("CDO", 8.308666666666667, -1.1, 196.66)
    CEB = MagdasStation("CEB", 8.260666666666667, 2.53, 195.06)
    DAV = MagdasStation("DAV", 8.36, -1.02, 196.54)
    DAW = MagdasStation("DAW", 8.728, -21.91, 202.81)
    EUS = MagdasStation("EUS", -2.562000000000003, -3.64, 34.21)
    EWA = MagdasStation("EWA", -10.5333333333333, 21.67, 269.52)
    GSI = MagdasStation("GSI", 6.507333333333333, -7.53, 169.49)
    HLN = MagdasStation("HLN", 8.103333333333333, 16.86, 193.05)
    HUA = MagdasStation("HUA", -5.01933333333333, -2.34, 357.39)
    ICA = MagdasStation("ICA", -5.04933333333333, -1.56, 356.16)
    ILR = MagdasStation("ILR", 0.312, -1.82, 76.8)
    KRT = MagdasStation("KRT", 2.1546666666666665, 5.69, 103.8)
    LAG = MagdasStation("LAG", 0.218, -3.04, 75.33)
    LGZ = MagdasStation("LGZ", 8.249333333333333, 3.54, 195.56)
    LKW = MagdasStation("LKW", 6.652, -2.32, 171.29)
    LWA = MagdasStation("LWA", 6.937333333333333, -16.19, 175.33)
    MND = MagdasStation("MND", 8.322666666666666, -6.91, 196.06)
    MUT = MagdasStation("MUT", 8.068, 6.79, 192.25)
    NAB = MagdasStation("NAB", 2.432, -10.65, 108.18)
    PRP = MagdasStation("PRP", 7.96, -12.38, 190.75)
    SCN = MagdasStation("SCN", 6.6866666666666665, -12.11, 171.66)
    TGG = MagdasStation("TGG", 8.117333333333334, 10.26, 193.05)
    TIR = MagdasStation("TIR", 5.13, -0.37, 149.11)
    YAP = MagdasStation("YAP", 9.205333333333333, 1.49, 209.06)

    @property
    def code(self):
        return self.value.code

    @property
    def time_diff(self):
        return self.value.time_diff

    @property
    def gm_lat(self):
        return self.value.gm_lat

    @property
    def gm_lon(self):
        return self.value.gm_lon

    def is_dip(self) -> bool:
        return abs(self.gm_lat) < 3

    def is_offdip(self) -> bool:
        """
        In the referenced paper, offdip is defined as 3 <= |gm_lat| <= 10,
        but due to limited station data, the range is extended to 15 degrees.
        """
        return 3 <= abs(self.gm_lat) <= 15

    @classmethod
    def is_included(cls, station_code: str) -> bool:
        return station_code in [station.code for station in cls]
