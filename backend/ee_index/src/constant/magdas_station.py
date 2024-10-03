from dataclasses import dataclass
from enum import Enum


@dataclass
class MagdasStation:
    code: str
    time_diff: float
    gm_lat: float


class EeIndexStation(MagdasStation, Enum):
    AAB = "AAB", 2.585333333333333, 0.18
    ABU = "ABU", 0.49266666666666664, -1.53
    AMA = "AMA", 8.622, 21.11
    ANC = "ANC", -5.143333333333333, 0.77
    BCL = "BCL", 7.047333333333333, -0.66
    BKL = "BKL", 6.820666666666667, -15.13
    CDO = "CDO", 8.308666666666667, -1.1
    CEB = "CEB", 8.260666666666667, 2.53
    DAV = "DAV", 8.36, -1.02
    DAW = "DAW", 8.728, -21.91
    EUS = "EUS", -2.562000000000003, -3.64
    EWA = "EWA", -10.5333333333333, 21.67
    GSI = "GSI", 6.507333333333333, -7.53
    HLN = "HLN", 8.103333333333333, 16.86
    ICA = "ICA", -5.04933333333333, -1.56
    ILR = "ILR", 0.312, -1.82
    KRT = "KRT", 2.1546666666666665, 5.69
    LAG = "LAG", 0.218, -3.04
    LGZ = "LGZ", 8.249333333333333, 3.54
    LKW = "LKW", 6.652, -2.32
    LWA = "LWA", 6.937333333333333, -16.19
    MND = "MND", 8.322666666666666, -6.91
    MUT = "MUT", 8.068, 6.79
    NAB = "NAB", 2.432, -10.65
    PRP = "PRP", 7.96, -12.38
    SCN = "SCN", 6.6866666666666665, -12.11
    TGG = "TGG", 8.117333333333334, 10.26
    TIR = "TIR", 5.13, -0.37
    YAP = "YAP", 9.205333333333333, 1.49

    @classmethod
    def is_included(cls, station_code: str) -> bool:
        return station_code in [station.code for station in EeIndexStation]
