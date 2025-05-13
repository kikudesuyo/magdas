import warnings

import numpy as np


class NanCalculator:
    @staticmethod
    def nanmedian(array) -> np.float32:
        """ignore nan values

        Note:
          np.nanmedian() returns nan if all values are nan
          Avoid RuntimeWarnings: All-NaN slice encountered
        """
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning, append=True)
            median = np.nanmedian(array)
        return np.float32(median)

    @staticmethod
    def nanmean(array, axis=0):
        """ignore nan values

        Note:
          np.nanmean() returns nan if all values are nan
          Avoid RuntimeWarnings: Mean of empty slice
        """
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning, append=True)
            mean = np.nanmean(array, axis=axis)
        return mean
