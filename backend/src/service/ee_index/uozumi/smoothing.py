import numpy as np


def remove_outliers(rough_arrray):
    rough_arrray[rough_arrray < -300] = np.nan
    rough_arrray[rough_arrray > 300] = np.nan
    return rough_arrray
