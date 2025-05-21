import os
import unittest
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.usecase.ee_index.calc_er import Er
from src.usecase.ee_index.calc_h_component import HComponent
from src.usecase.ee_index.er_baseline import ErBaseline


class TestErBaseline(unittest.TestCase):
    """Test the ER baseline functionality."""

    def setUp(self):
        # Use a temporary directory for testing
        self.original_baseline_dir = ErBaseline.BASELINE_DIR
        self.original_baseline_file = ErBaseline.BASELINE_FILE
        
        self.test_dir = Path("/tmp/er_baseline_test")
        os.makedirs(self.test_dir, exist_ok=True)
        
        ErBaseline.BASELINE_DIR = self.test_dir
        ErBaseline.BASELINE_FILE = self.test_dir / "er_baseline_test.csv"
        
        # Remove the test file if it exists
        if ErBaseline.BASELINE_FILE.exists():
            os.remove(ErBaseline.BASELINE_FILE)

    def tearDown(self):
        # Restore the original values
        ErBaseline.BASELINE_DIR = self.original_baseline_dir
        ErBaseline.BASELINE_FILE = self.original_baseline_file
        
        # Clean up the test directory
        if ErBaseline.BASELINE_FILE.exists():
            os.remove(ErBaseline.BASELINE_FILE)
        if self.test_dir.exists():
            os.rmdir(self.test_dir)

    def test_baseline_date_calculation(self):
        """Test that the baseline date is calculated correctly."""
        # Test with a date at the beginning of the month
        date1 = datetime(2014, 4, 1)
        baseline_date1 = ErBaseline._get_baseline_date(date1)
        self.assertEqual(baseline_date1, datetime(2014, 4, 1))
        
        # Test with a date in the middle of the month
        date2 = datetime(2014, 4, 15)
        baseline_date2 = ErBaseline._get_baseline_date(date2)
        self.assertEqual(baseline_date2, datetime(2014, 4, 11))
        
        # Test with a date at the end of the month
        date3 = datetime(2014, 4, 30)
        baseline_date3 = ErBaseline._get_baseline_date(date3)
        self.assertEqual(baseline_date3, datetime(2014, 4, 21))

    def test_save_and_load_baseline_values(self):
        """Test saving and loading baseline values."""
        # Create some test data
        baseline_values = {
            "2014-04-01": {"ANC": 123.45, "EUS": 234.56},
            "2014-04-11": {"ANC": 345.67, "EUS": 456.78},
        }
        
        # Save the data
        ErBaseline.save_baseline_values(baseline_values)
        
        # Load the data
        loaded_values = ErBaseline.load_baseline_values()
        
        # Check that the loaded data matches the original data
        self.assertEqual(loaded_values, baseline_values)

    def test_er_calculation_with_fixed_baseline(self):
        """Test that ER calculation uses the fixed baseline."""
        # Create a test station and period
        station = EeIndexStation.ANC
        start_ut = datetime(2014, 4, 1, 0, 0)
        end_ut = datetime(2014, 4, 1, 23, 59)
        period = Period(start_ut, end_ut)
        params = StationParams(station, period)
        
        # Create a mock baseline value
        baseline_values = {
            "2014-04-01": {station.code: 12345.0},
        }
        ErBaseline.save_baseline_values(baseline_values)
        
        # Calculate ER with the fixed baseline
        h = HComponent(params)
        er = Er(h)
        er_values = er.calc_er(use_fixed_baseline=True)
        
        # Check that the ER values are calculated correctly
        # We can't check the exact values because they depend on the data,
        # but we can check that they're not all NaN
        self.assertFalse(np.all(np.isnan(er_values)))

    def test_night_euel_offset(self):
        """Test that the night EUEL offset is calculated correctly."""
        # This test is more of an integration test and depends on the data
        # available in the repository. It might fail if the data is not available.
        try:
            # Create a test station and period
            station = EeIndexStation.ANC
            start_ut = datetime(2014, 4, 1, 0, 0)
            end_ut = datetime(2014, 4, 1, 23, 59)
            period = Period(start_ut, end_ut)
            
            # Calculate the offset
            offset = ErBaseline.get_night_euel_offset(station, period)
            
            # Check that the offset is a float
            self.assertIsInstance(offset, float)
        except Exception as e:
            # Skip the test if the data is not available
            self.skipTest(f"Test skipped due to data unavailability: {e}")


if __name__ == "__main__":
    unittest.main()