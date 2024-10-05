from pydantic import BaseModel


class Ee_index(BaseModel):
    date: str
    station: str
