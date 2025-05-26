from dataclasses import dataclass
from datetime import date
from glob import glob

import numpy as np
from src.constants.ee_index import MAX_RAW_H, MIN_RAW_H
from src.constants.time_relation import TimeUnit
from src.repository.raw_file_reader import read_raw_min_data
from src.utils.path import generate_parent_abs_path


@dataclass
class GM:
    h: np.ndarray
    d: np.ndarray
    z: np.ndarray
    f: np.ndarray


class GMDataLoader:
    def __init__(self, station_code: str, ut_date: date):
        self.station_code = station_code
        self.ut_date = ut_date
        self.gm = self._load_gm()

    def _load_gm(self) -> GM:
        year = self.ut_date.strftime("%Y")
        month = self.ut_date.strftime("%m")
        day = self.ut_date.strftime("%d")
        filenames = glob(
            generate_parent_abs_path(
                f"/Storage/ee_index/{self.station_code}/Min/{year}/{self.station_code}_MIN_{year}{month}{day}*.mgd"
            )
        )
        if len(filenames) == 0:
            nan_arr = np.full(TimeUnit.ONE_DAY.min, np.NaN)
            return GM(h=nan_arr, d=nan_arr, z=nan_arr, f=nan_arr)
        if len(filenames) > 1:
            raise FileNotFoundError(
                f"Multiple files found for {self.station_code} at {self.ut_date}: {filenames}"
            )
        try:
            raw_data = read_raw_min_data(filenames[0])[:, :4]  # Get only h, d, z, f
            data = self._sanitize(raw_data)
            h, d, z, f = data.T
            return GM(h, d, z, f)
        except ValueError:  # Handle file format errors
            nan_arr = np.full(TimeUnit.ONE_DAY.min, np.NaN)
            return GM(nan_arr, nan_arr, nan_arr, nan_arr)

    def _sanitize(self, data: np.ndarray) -> np.ndarray:
        """Sanitize the data by replacing invalid values with NaN."""
        return np.where((data <= MIN_RAW_H) | (data >= MAX_RAW_H), np.NaN, data)

    @property
    def h(self) -> np.ndarray:
        return self.gm.h

    @property
    def d(self) -> np.ndarray:
        """Get the d component for the day."""
        return self.gm.d

    @property
    def z(self) -> np.ndarray:
        """Get the z component for the day."""
        return self.gm.z

    @property
    def f(self) -> np.ndarray:
        """Get the f component for the day."""
        return self.gm.f
