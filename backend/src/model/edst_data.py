import numpy as np
from pydantic import BaseModel, ConfigDict


class EdstData(BaseModel):
    array: np.ndarray

    # numpyを使うためにConfigDictを設定
    model_config = ConfigDict(arbitrary_types_allowed=True)
