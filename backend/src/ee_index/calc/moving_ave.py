import numpy as np


def calc_moving_ave(data, window):
    weights = np.ones(window) / window
    valid_cnt = np.convolve(~np.isnan(data), weights, mode="same")
    data_filled = np.nan_to_num(data, nan=0)
    moving_sum = np.convolve(data_filled, weights, mode="same")
    moving_avg = np.divide(moving_sum, valid_cnt, where=(valid_cnt > 0))
    moving_avg[valid_cnt == 0] = np.nan
    return moving_avg
