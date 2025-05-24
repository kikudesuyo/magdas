import csv
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
from src.constants.time_relation import TimeUnit
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.usecase.ee_index.calc_er import Er
from src.usecase.ee_index.calc_h_component import HComponent
from src.usecase.ee_index.nan_calculator import NanCalculator


class ErBaseline:
    """Class to manage ER baseline values.
    
    The baseline values are stored in a CSV file and updated every 10 days.
    The CSV file format is:
    date,station1,station2,...
    YYYY-MM-DD,value1,value2,...
    """
    
    BASELINE_DIR = Path("/workspace/magdas/backend/data/er_baseline")
    BASELINE_FILE = BASELINE_DIR / "er_baseline.csv"
    UPDATE_INTERVAL_DAYS = 10
    
    @classmethod
    def ensure_baseline_dir(cls) -> None:
        """Ensure the baseline directory exists."""
        os.makedirs(cls.BASELINE_DIR, exist_ok=True)
    
    @classmethod
    def get_baseline_file_path(cls) -> Path:
        """Get the path to the baseline file."""
        cls.ensure_baseline_dir()
        return cls.BASELINE_FILE
    
    @classmethod
    def load_baseline_values(cls) -> Dict[str, Dict[str, float]]:
        """Load baseline values from the CSV file.
        
        Returns:
            Dict[str, Dict[str, float]]: A dictionary mapping dates to station values.
                {
                    "2014-01-01": {
                        "ANC": 123.45,
                        "EUS": 234.56,
                        ...
                    },
                    ...
                }
        """
        baseline_file = cls.get_baseline_file_path()
        if not baseline_file.exists():
            return {}
        
        baseline_values = {}
        with open(baseline_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                date_str = row.pop("date")
                station_values = {station: float(value) for station, value in row.items() if value}
                baseline_values[date_str] = station_values
        
        return baseline_values
    
    @classmethod
    def save_baseline_values(cls, baseline_values: Dict[str, Dict[str, float]]) -> None:
        """Save baseline values to the CSV file.
        
        Args:
            baseline_values: A dictionary mapping dates to station values.
        """
        baseline_file = cls.get_baseline_file_path()
        
        # Get all station codes
        all_stations = set()
        for station_values in baseline_values.values():
            all_stations.update(station_values.keys())
        
        # Sort stations for consistent output
        sorted_stations = sorted(all_stations)
        
        with open(baseline_file, "w", newline="") as f:
            fieldnames = ["date"] + sorted_stations
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for date_str, station_values in sorted(baseline_values.items()):
                row = {"date": date_str}
                row.update(station_values)
                writer.writerow(row)
    
    @classmethod
    def calculate_baseline(cls, station: EeIndexStation, date: datetime) -> float:
        """Calculate the baseline value for a station on a specific date.
        
        This calculates the median of the H component for the station over a 24-hour period.
        
        Args:
            station: The station to calculate the baseline for.
            date: The date to calculate the baseline for.
            
        Returns:
            float: The baseline value.
        """
        start_ut = datetime(date.year, date.month, date.day, 0, 0)
        end_ut = start_ut + timedelta(days=1) - timedelta(minutes=1)
        period = Period(start_ut, end_ut)
        params = StationParams(station, period)
        
        h = HComponent(params)
        h_component = h.to_equatorial_h()
        baseline = NanCalculator.nanmedian(h_component)
        
        return float(baseline)
    
    @classmethod
    def get_or_calculate_baseline(
        cls, station: EeIndexStation, date: datetime
    ) -> float:
        """Get the baseline value for a station on a specific date.
        
        If the baseline value is not available in the CSV file, it will be calculated
        and saved to the file.
        
        Args:
            station: The station to get the baseline for.
            date: The date to get the baseline for.
            
        Returns:
            float: The baseline value.
        """
        # Find the nearest baseline date (every 10 days)
        baseline_date = cls._get_baseline_date(date)
        date_str = baseline_date.strftime("%Y-%m-%d")
        
        # Load existing baseline values
        baseline_values = cls.load_baseline_values()
        
        # Check if the baseline value exists
        if date_str in baseline_values and station.code in baseline_values[date_str]:
            return baseline_values[date_str][station.code]
        
        # Calculate the baseline value
        baseline = cls.calculate_baseline(station, baseline_date)
        
        # Save the baseline value
        if date_str not in baseline_values:
            baseline_values[date_str] = {}
        baseline_values[date_str][station.code] = baseline
        cls.save_baseline_values(baseline_values)
        
        return baseline
    
    @classmethod
    def _get_baseline_date(cls, date: datetime) -> datetime:
        """Get the baseline date for a given date.
        
        The baseline date is the nearest date that is a multiple of UPDATE_INTERVAL_DAYS
        from the beginning of the month.
        
        Args:
            date: The date to get the baseline date for.
            
        Returns:
            datetime: The baseline date.
        """
        # Start from the beginning of the month
        month_start = datetime(date.year, date.month, 1)
        
        # Calculate the number of days from the beginning of the month
        days_from_month_start = (date - month_start).days
        
        # Calculate the nearest baseline date
        baseline_day = (days_from_month_start // cls.UPDATE_INTERVAL_DAYS) * cls.UPDATE_INTERVAL_DAYS + 1
        
        # If the baseline day is beyond the current date, use the previous baseline
        if baseline_day > date.day:
            baseline_day = max(1, baseline_day - cls.UPDATE_INTERVAL_DAYS)
        
        return datetime(date.year, date.month, baseline_day)
    
    @classmethod
    def get_night_euel_offset(cls, station: EeIndexStation, period: Period) -> float:
        """Calculate the offset to apply to EUEL values to make nighttime values closer to 0.
        
        Args:
            station: The station to calculate the offset for.
            period: The period to calculate the offset for.
            
        Returns:
            float: The offset value.
        """
        params = StationParams(station, period)
        h = HComponent(params)
        er = Er(h)
        
        # Get nighttime EUEL values
        night_er = er.extract_night_er()
        
        # Calculate the median of nighttime values
        with np.errstate(all='ignore'):
            offset = NanCalculator.nanmedian(night_er)
        
        return float(offset)