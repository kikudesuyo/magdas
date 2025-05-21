# ER Baseline Values

This directory contains CSV files with ER (Equatorial Electrojet) baseline values for different stations.

## Background

ER values are calculated by subtracting a baseline value from the equatorial H component of the magnetic field. Previously, this baseline was calculated for each time period, which caused inconsistency in the ER values when analyzing different time periods.

To solve this issue, we now store baseline values in CSV files and use them consistently across all calculations. Baseline values are calculated every 10 days, as recommended by experts.

## File Format

The baseline values are stored in a CSV file with the following format:

```
date,ANC,EUS,...
2014-01-01,12345.67,23456.78,...
2014-01-11,12346.78,23457.89,...
...
```

Where:
- `date` is the date in YYYY-MM-DD format
- Each column after that contains the baseline value for a specific station

## Generating Baseline Values

To generate baseline values for a range of dates, use the `generate_er_baselines.py` script:

```bash
cd backend
python scripts/generate_er_baselines.py --start-date 2014-01-01 --end-date 2014-12-31 --interval 10 --stations ANC EUS
```

This will calculate baseline values for the specified stations (ANC and EUS in this example) for every 10 days from January 1, 2014 to December 31, 2014.

## Implementation Details

The baseline values are managed by the `ErBaseline` class in `src/usecase/ee_index/er_baseline.py`. This class provides methods to:

- Load and save baseline values
- Calculate baseline values for a specific date and station
- Get the baseline value for a specific date and station (using the closest available baseline within 10 days)
- Calculate the offset to apply to EUEL values to make nighttime values closer to 0

The `Er` class in `src/usecase/ee_index/calc_er.py` uses these baseline values when calculating ER values, and the `Euel` class in `src/usecase/ee_index/calc_euel.py` uses the nighttime offset to adjust EUEL values.