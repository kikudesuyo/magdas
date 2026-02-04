from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Organization(Enum):
    MAGDAS = "MAGDAS"
    INTERMAG = "INTERMAG"
    GFZ = "GFZ"


@dataclass(frozen=True)
class Station:
    code: str
    name: str
    nation: str
    organization: Organization
    gg_lat: float
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
        "Addis Ababa",
        "Ethiopia",
        Organization.MAGDAS,
        gg_lat=9.04,
        gg_lon=38.77,
        gm_lat=5.41,
        gm_lon=112.54,
        dip_lat=1.21,
    )
    ABU = Station(
        "ABU",
        "Abuja",
        "Nigeria",
        Organization.MAGDAS,
        gg_lat=8.99,
        gg_lon=7.39,
        gm_lat=-0.54,
        gm_lon=81.31,
        dip_lat=-3.36,
    )
    AMA = Station(
        "AMA",
        "Amami-Oh-shima",
        "Japan",
        Organization.MAGDAS,
        gg_lat=28.17,
        gg_lon=129.33,
        gm_lat=21.11,
        gm_lon=200.88,
        dip_lat=23.39,
    )
    ANC = Station(
        "ANC",
        "Ancon",
        "Peru",
        Organization.MAGDAS,
        gg_lat=-11.77,
        gg_lon=-77.15,
        gm_lat=-2.11,
        gm_lon=355.57,
        dip_lat=0.13,
    )
    BCL = Station(
        "BCL",
        "Bac Lieu",
        "Vietnam",
        Organization.MAGDAS,
        gg_lat=9.32,
        gg_lon=105.71,
        gm_lat=-0.36,
        gm_lon=178.36,
        dip_lat=2.5,
    )
    BKL = Station(
        "BKL",
        "Bengkulu",
        "Indonesia",
        Organization.MAGDAS,
        gg_lat=-3.8,
        gg_lon=102.31,
        gm_lat=-15.13,
        gm_lon=173.6,
        dip_lat=-13.64,
    )
    CDO = Station(
        "CDO",
        "Cagayan De Oro",
        "Philippines",
        Organization.MAGDAS,
        gg_lat=8.46,
        gg_lon=124.63,
        gm_lat=-0.8,
        gm_lon=197.06,
        dip_lat=1.41,
    )
    CEB = Station(
        "CEB",
        "Cebu",
        "Philippines",
        Organization.MAGDAS,
        gg_lat=10.36,
        gg_lon=123.91,
        gm_lat=1.06,
        gm_lon=196.26,
        dip_lat=3.59,
    )
    DAV = Station(
        "DAV",
        "Davao",
        "Philippines",
        Organization.MAGDAS,
        gg_lat=7.0,
        gg_lon=125.4,
        gm_lat=-2.22,
        gm_lon=197.9,
        dip_lat=-0.27,
    )
    DAW = Station(
        "DAW",
        "Darwin",
        "Australia",
        Organization.MAGDAS,
        gg_lat=-12.41,
        gg_lon=130.92,
        gm_lat=-21.91,
        gm_lon=202.81,
        dip_lat=-22.4,
    )
    EUS = Station(
        "EUS",
        "Eusebio",
        "Brazil",
        Organization.MAGDAS,
        gg_lat=-3.88,
        gg_lon=-38.43,
        gm_lat=4.14,
        gm_lon=34.21,
        dip_lat=-9.41,
    )
    EWA = Station(
        "EWA",
        "Ewa beach",
        "USA",
        Organization.MAGDAS,
        gg_lat=21.32,
        gg_lon=-158.0,
        gm_lat=21.63,
        gm_lon=269.45,
        dip_lat=21.37,
    )
    GSI = Station(
        "GSI",
        "Gunung Sitoli",
        "Indonesia",
        Organization.MAGDAS,
        gg_lat=1.3,
        gg_lon=97.58,
        gm_lat=-8.25,
        gm_lon=170.1,
        dip_lat=-7.65,
    )
    HLN = Station(
        "HLN",
        "Hualien",
        "Taiwan",
        Organization.MAGDAS,
        gg_lat=23.9,
        gg_lon=121.55,
        gm_lat=16.86,
        gm_lon=193.05,
        dip_lat=19.37,
    )
    HUA = Station(
        "HUA",
        "Huancayo",
        "Peru",
        Organization.MAGDAS,
        gg_lat=-12.02,
        gg_lon=-75.29,
        gm_lat=-2.34,
        gm_lon=357.39,
        dip_lat=-0.17,
    )
    ICA = Station(
        "ICA",
        "Ica",
        "Peru",
        Organization.MAGDAS,
        gg_lat=-14.09,
        gg_lon=-75.74,
        gm_lat=-4.42,
        gm_lon=356.97,
        dip_lat=-2.07,
    )
    ILR = Station(
        "ILR",
        "Ilorin",
        "Nigeria",
        Organization.MAGDAS,
        gg_lat=8.5,
        gg_lon=4.68,
        gm_lat=10.5,
        gm_lon=78.9,
        dip_lat=-4.16,
    )
    KRT = Station(
        "KRT",
        "Khartoum",
        "Sudan",
        Organization.MAGDAS,
        gg_lat=15.33,
        gg_lon=32.32,
        gm_lat=12.64,
        gm_lon=107.27,
        dip_lat=7.91,
    )
    LAG = Station(
        "LAG",
        "Lagos",
        "Nigeria",
        Organization.MAGDAS,
        gg_lat=6.48,
        gg_lon=3.27,
        gm_lat=-3.04,
        gm_lon=75.33,
        dip_lat=-6.93,
    )
    LGZ = Station(
        "LGZ",
        "Legazpi",
        "Philippines",
        Organization.MAGDAS,
        gg_lat=13.15,
        gg_lon=123.74,
        gm_lat=3.84,
        gm_lon=195.96,
        dip_lat=6.76,
    )
    LKW = Station(
        "LKW",
        "Langkawi",
        "Malaysia",
        Organization.MAGDAS,
        gg_lat=6.3,
        gg_lon=99.78,
        gm_lat=-3.3,
        gm_lon=172.44,
        dip_lat=-1.41,
    )
    LWA = Station(
        "LWA",
        "Liwa",
        "Indonesia",
        Organization.MAGDAS,
        gg_lat=-5.02,
        gg_lon=104.06,
        gm_lat=-16.19,
        gm_lon=175.33,
        dip_lat=-14.99,
    )
    MND = Station(
        "MND",
        "Manado",
        "Indonesia",
        Organization.MAGDAS,
        gg_lat=1.44,
        gg_lon=124.84,
        gm_lat=-7.8,
        gm_lon=197.63,
        dip_lat=-6.5,
    )
    MUT = Station(
        "MUT",
        "Muntinlupa",
        "Philippines",
        Organization.MAGDAS,
        gg_lat=14.37,
        gg_lon=121.02,
        gm_lat=4.95,
        gm_lon=193.26,
        dip_lat=8.32,
    )
    NAB = Station(
        "NAB",
        "Nairobi",
        "Kenya",
        Organization.MAGDAS,
        gg_lat=-1.16,
        gg_lon=36.48,
        gm_lat=-10.65,
        gm_lon=108.18,
        dip_lat=-12.23,
    )
    PRP = Station(
        "PRP",
        "Pare Pare",
        "Indonesia",
        Organization.MAGDAS,
        gg_lat=-3.6,
        gg_lon=119.4,
        gm_lat=-12.38,
        gm_lon=190.75,
        dip_lat=-12.23,
    )
    SCN = Station(
        "SCN",
        "Sicincin",
        "Indonesia",
        Organization.MAGDAS,
        gg_lat=-0.55,
        gg_lon=100.3,
        gm_lat=-10.16,
        gm_lon=172.81,
        dip_lat=-9.78,
    )
    TGG = Station(
        "TGG",
        "Tuguegarao",
        "Philippines",
        Organization.MAGDAS,
        gg_lat=17.66,
        gg_lon=121.76,
        gm_lat=10.26,
        gm_lon=193.05,
        dip_lat=12.06,
    )
    TIR = Station(
        "TIR",
        "Tirunelveli",
        "India",
        Organization.MAGDAS,
        gg_lat=8.7,
        gg_lon=77.8,
        gm_lat=0.25,
        gm_lon=150.8,
        dip_lat=1.74,
    )
    YAP = Station(
        "YAP",
        "Yap Island",
        "FSM",
        Organization.MAGDAS,
        gg_lat=9.5,
        gg_lon=138.08,
        gm_lat=1.14,
        gm_lon=210.25,
        dip_lat=1.97,
    )

    # INTERMAG観測点

    #  gm_lat は dip_latを参照
    # gm_lon は不明のため None とする
    TTB = Station(
        "TTB",
        "Tatuoca",
        "Brazil",
        Organization.INTERMAG,
        gg_lat=None,
        gg_lon=-48.51,
        gm_lat=None,
        gm_lon=None,
        dip_lat=-0.72,
    )
    KOU = Station(
        "KOU",
        "Kourou",
        "French Guiana",
        Organization.GFZ,
        gg_lat=None,
        gg_lon=-52.73,
        gm_lat=None,
        gm_lon=None,
        dip_lat=7.59,
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

    @property
    def organization(self) -> Organization:
        return self.value.organization

    def is_dip(self) -> bool:
        return abs(self.dip_lat) < 3

    def is_offdip(self) -> bool:
        """
        In the referenced paper, offdip is defined as 3 <= |gm_lat| <= 10,
        but due to limited station data, the range is extended to 15 degrees.
        """
        return 3 <= abs(self.dip_lat) <= 15
