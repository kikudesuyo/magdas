from pydantic import BaseModel


class DailyEeIndex(BaseModel):
    date: str
    station: str


class RangeEeIndex(BaseModel):
    startDate: str
    endDate: str
    station: str
