from dataclasses import dataclass
from enum import Enum


@dataclass
class RegionInfo:
    code: str
    label: str


class Region(Enum):
    SOUTH_AMERICA = RegionInfo("south_america", "South America")
    SOUTHEAST_ASIA = RegionInfo("southeast_asia", "Southeast Asia")

    @property
    def label(self):
        return self.value.label

    @property
    def code(self):
        return self.value.code

    @classmethod
    def from_code(cls, code: str):
        for region in cls:
            if region.code == code:
                return region
        raise ValueError(f"Invalid region code: {code}")
