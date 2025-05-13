import numpy as np


def interpolate_nan(arr: np.ndarray) -> np.ndarray:
    x = np.arange(len(arr))
    nan_indices = np.isnan(arr)
    x_valid = x[~nan_indices]
    y_valid = arr[~nan_indices]
    arr[nan_indices] = np.interp(x[nan_indices], x_valid, y_valid)
    return arr
