import numpy as np


def interpolate_nan(arr: np.ndarray) -> np.ndarray:
    result = arr.copy()  # 副作用防止
    x = np.arange(result.size)

    nan_mask = np.isnan(result)
    valid_mask = ~nan_mask

    if np.count_nonzero(valid_mask) < 2:
        return result

    result[nan_mask] = np.interp(
        x[nan_mask],
        x[valid_mask],
        result[valid_mask],
        left=np.nan,
        right=np.nan,
    )
    return result
