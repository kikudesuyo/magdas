from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Organization(Enum):
    MAGDAS = "MAGDAS"
    INTERMAG = "INTERMAG"
    SUPERMAG = "SUPERMAG"


@dataclass(frozen=True)
class Station:
    code: str
    name: str
    nation: str
    organization: Organization
    gg_lon: float
    gm_lat: Optional[float]
    gm_lon: Optional[float]
    dip_lat: float


class EeIndexStation(Enum):
    """
    Ref: https://data.i-spes.kyushu-u.ac.jp/eeindex/SG_v11_No1_2016-pp-37-47.pdf
    """

    # MAGDAS観測点 藤本論文2015での観測点データ
    AAB = Station(
        "AAB",
        "Adis Ababa",
        "Ethiopia",
        Organization.MAGDAS,
        38.77,
        5.41,
        112.54,
        1.21,
    )
    ABU = Station(
        "ABU",
        "Abuja",
        "Nigeria",
        Organization.MAGDAS,
        7.39,
        -0.54,
        81.31,
        -3.36,
    )
    AMA = Station(
        "AMA",
        "Amami-Oh-shima",
        "Japan",
        Organization.MAGDAS,
        129.33,
        21.11,
        200.88,
        23.39,
    )
    ANC = Station(
        "ANC", "Ancon", "Peru", Organization.MAGDAS, -77.15, -2.11, 355.57, 0.13
    )
    BCL = Station(
        "BCL", "Bac Lieu", "Vietnam", Organization.MAGDAS, 105.71, -0.36, 178.36, 2.5
    )
    BKL = Station(
        "BKL",
        "Bengkulu",
        "Indonesia",
        Organization.MAGDAS,
        102.31,
        -15.13,
        173.6,
        -13.64,
    )
    CDO = Station(
        "CDO",
        "Cagayan De Oro",
        "Philippines",
        Organization.MAGDAS,
        124.63,
        -0.8,
        197.06,
        1.41,
    )
    CEB = Station(
        "CEB",
        "Cebu",
        "Philippines",
        Organization.MAGDAS,
        123.91,
        1.06,
        196.26,
        3.59,
    )
    DAV = Station(
        "DAV", "Davao", "Philippines", Organization.MAGDAS, 125.4, -2.22, 197.9, -0.27
    )
    DAW = Station(
        "DAW", "Darwin", "Australia", Organization.MAGDAS, 130.92, -21.91, 202.81, -22.4
    )
    EUS = Station(
        "EUS",
        "Eusebio",
        "Brazil",
        Organization.MAGDAS,
        -38.43,
        4.14,
        34.21,
        -9.41,
    )
    EWA = Station(
        "EWA",
        "Ewa beach",
        "USA",
        Organization.MAGDAS,
        -158.0,
        21.63,
        269.45,
        21.37,
    )
    GSI = Station(
        "GSI",
        "Gunung Sitoli",
        "Indonesia",
        Organization.MAGDAS,
        97.58,
        -8.25,
        170.1,
        -7.65,
    )
    HLN = Station(
        "HLN",
        "Hualien",
        "Taiwan",
        Organization.MAGDAS,
        121.55,
        16.86,
        193.05,
        19.37,
    )
    HUA = Station(
        "HUA",
        "Huancayo",
        "Peru",
        Organization.MAGDAS,
        -75.29,
        -2.34,
        357.39,
        -0.17,
    )
    ICA = Station(
        "ICA",
        "Ica",
        "Peru",
        Organization.MAGDAS,
        -75.74,
        -4.42,
        356.97,
        -2.07,
    )
    ILR = Station(
        "ILR", "Ilorin", "Nigeria", Organization.MAGDAS, 4.68, 10.5, 78.9, -4.16
    )
    KRT = Station(
        "KRT",
        "Khartoum",
        "Sudan",
        Organization.MAGDAS,
        32.32,
        12.64,
        107.27,
        7.91,
    )
    LAG = Station(
        "LAG", "Lagos", "Nigeria", Organization.MAGDAS, 3.27, -3.04, 75.33, -6.93
    )
    LGZ = Station(
        "LGZ",
        "Legazpi",
        "Philippines",
        Organization.MAGDAS,
        123.74,
        3.84,
        195.96,
        6.76,
    )
    LKW = Station(
        "LKW", "Langkawi", "Malaysia", Organization.MAGDAS, 99.78, -3.3, 172.44, -1.41
    )
    LWA = Station(
        "LWA", "Liwa", "Indonesia", Organization.MAGDAS, 104.06, -16.19, 175.33, -14.99
    )
    MND = Station(
        "MND",
        "Manado",
        "Indonesia",
        Organization.MAGDAS,
        124.84,
        -7.8,
        197.63,
        -6.5,
    )
    MUT = Station(
        "MUT",
        "Muntinlupa",
        "Philippines",
        Organization.MAGDAS,
        121.02,
        4.95,
        193.26,
        8.32,
    )
    NAB = Station(
        "NAB", "Nairobi", "Kenya", Organization.MAGDAS, 36.48, -10.65, 108.18, -12.23
    )
    PRP = Station(
        "PRP",
        "Pare Pare",
        "Indonesia",
        Organization.MAGDAS,
        119.4,
        -12.38,
        190.75,
        -12.23,
    )
    SCN = Station(
        "SCN",
        "Sicincin",
        "Indonesia",
        Organization.MAGDAS,
        100.3,
        -10.16,
        172.81,
        -9.78,
    )
    TGG = Station(
        "TGG",
        "Tuguegarao",
        "Philippines",
        Organization.MAGDAS,
        121.76,
        10.26,
        193.05,
        12.06,
    )
    TIR = Station(
        "TIR", "Tirunelveli", "India", Organization.MAGDAS, 77.8, 0.25, 150.8, 1.74
    )
    YAP = Station(
        "YAP",
        "Yap Island",
        "FSM",
        Organization.MAGDAS,
        138.08,
        1.14,
        210.25,
        1.97,
    )

    # SUPERMAG観測点

    #  gm_lat は dip_latを参照
    # gm_lon は不明のため None とする
    TTB = Station(
        "TTB", "Tatuoca", "Brazil", Organization.SUPERMAG, -48.51, None, None, -0.72
    )

    @property
    def code(self):
        return self.value.code

    @property
    def time_diff(self):
        ONE_HOUR = 15
        return self.value.gg_lon / ONE_HOUR

    @property
    def gm_lat(self):
        return self.value.gm_lat

    @property
    def gm_lon(self):
        return self.value.gm_lon

    @property
    def dip_lat(self):
        return self.value.dip_lat

    def is_dip(self) -> bool:
        return abs(self.dip_lat) < 3

    def is_offdip(self) -> bool:
        """
        In the referenced paper, offdip is defined as 3 <= |gm_lat| <= 10,
        but due to limited station data, the range is extended to 15 degrees.
        """
        return 3 <= abs(self.dip_lat) <= 15
