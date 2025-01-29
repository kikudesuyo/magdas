from pydantic import BaseModel


class RangeEeIndex(BaseModel):
    startDate: str
    endDate: str
    station: str
