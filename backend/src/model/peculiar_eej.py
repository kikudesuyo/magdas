from datetime import date

from pydantic import BaseModel
from src.domain.region import Region


class PeculiarEejModel(BaseModel):
    date: date
    region: Region
    type: str
