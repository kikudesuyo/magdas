import numpy as np
import pandas as pd


def calc_moving_ave(data: np.ndarray, window: int, nan_threshold: int) -> np.ndarray:
    s = pd.Series(data)
    return s.rolling(window, min_periods=nan_threshold, center=True).mean().to_numpy()
