from dataclasses import dataclass
from enum import Enum


@dataclass
class Savgol:
    """Smooth"""

    length: int
    deg: int


class Smooth(Savgol, Enum):
    EE = 25, 3
