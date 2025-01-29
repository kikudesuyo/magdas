from pydantic import BaseModel


class DailyEeIndex(BaseModel):
    date: str
    station: str
