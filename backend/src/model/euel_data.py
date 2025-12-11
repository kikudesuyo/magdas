import numpy as np
from pydantic import BaseModel, ConfigDict
from src.domain.magdas_station import EeIndexStation
from src.domain.region import Region


class EuelData(BaseModel):
    region: Region
    station: EeIndexStation
    array: np.ndarray

    # numpyを使うためにConfigDictを設定
    model_config = ConfigDict(arbitrary_types_allowed=True)
