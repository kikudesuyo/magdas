from typing import Iterable, List

import numpy as np


def np_nan_to_none(values: np.ndarray) -> List[float | None]:
    return [None if np.isnan(x) else x for x in values]


def to_float(values: Iterable[float | None]) -> List[float | None]:
    return [float(x) if x is not None else None for x in values]


def sanitize_np(values: np.ndarray) -> List[float | None]:
    return to_float(np_nan_to_none(values))
