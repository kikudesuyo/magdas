#!/usr/bin/env python3
"""
Script to generate ER baseline values for a range of dates.

This script calculates and saves ER baseline values for all stations
over a specified date range, with a specified interval between calculations.
"""

import argparse
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.domain.magdas_station import EeIndexStation
from src.usecase.ee_index.er_baseline import ErBaseline


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate ER baseline values for a range of dates.")
    parser.add_argument(
        "--start-date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        default=datetime(2014, 1, 1),
        help="Start date in YYYY-MM-DD format (default: 2014-01-01)",
    )
    parser.add_argument(
        "--end-date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        default=datetime(2014, 12, 31),
        help="End date in YYYY-MM-DD format (default: 2014-12-31)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        help="Interval between baseline calculations in days (default: 10)",
    )
    parser.add_argument(
        "--stations",
        type=str,
        nargs="+",
        default=[station.code for station in EeIndexStation],
        help="Station codes to generate baselines for (default: all stations)",
    )
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_args()
    
    # Validate stations
    valid_stations = []
    for station_code in args.stations:
        try:
            station = next(s for s in EeIndexStation if s.code == station_code)
            valid_stations.append(station)
        except StopIteration:
            print(f"Warning: Unknown station code '{station_code}', skipping")
    
    if not valid_stations:
        print("Error: No valid stations specified")
        return
    
    # Ensure the baseline directory exists
    os.makedirs(ErBaseline.BASELINE_DIR, exist_ok=True)
    
    # Generate baselines for each station
    for station in valid_stations:
        print(f"Generating baselines for station {station.code}...")
        
        # Calculate baselines
        current_date = args.start_date
        while current_date <= args.end_date:
            try:
                baseline = ErBaseline.calculate_baseline(station, current_date)
                ErBaseline.get_or_calculate_baseline(station, current_date)
                print(f"  {current_date.strftime('%Y-%m-%d')}: {baseline:.2f}")
            except Exception as e:
                print(f"  Error calculating baseline for {current_date.strftime('%Y-%m-%d')}: {e}")
            
            # Move to the next date
            current_date += timedelta(days=args.interval)
    
    print("Done!")


if __name__ == "__main__":
    main()