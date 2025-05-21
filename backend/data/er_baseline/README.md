# ER Baseline Values

This directory contains the ER baseline values used for calculating ER and EUEL indices.

## Background

Previously, ER values were calculated using a dynamic baseline that changed every time the calculation was performed. This caused inconsistencies when detecting events, as the baseline would shift depending on the time period being analyzed.

The solution is to use fixed baseline values that are updated periodically (every 10 days), which provides a more stable reference for detecting events.

## Implementation

The baseline values are stored in a CSV file (`er_baseline.csv`) with the following format:

```
date,ANC,EUS,...
2014-04-01,12345.67,23456.78,...
2014-04-11,34567.89,45678.90,...
...
```

Where:
- `date` is the date of the baseline (YYYY-MM-DD)
- Each column represents a station code
- Each value is the baseline value for that station on that date

The baseline values are calculated as the median of the H component for each station over a 24-hour period.

## Usage

The baseline values are used in two ways:

1. For calculating ER values:
   - Instead of using the median of the current data, the fixed baseline value from the CSV file is used
   - This provides a more stable reference for detecting events

2. For adjusting EUEL values:
   - The nighttime EUEL values should ideally be close to 0
   - An offset is calculated based on the median of nighttime EUEL values
   - This offset is applied to all EUEL values to make the nighttime values closer to 0

## Maintenance

The baseline values are automatically updated when new data is processed. The update interval is set to 10 days, as recommended by domain experts.

If you need to manually update the baseline values, you can delete the CSV file and it will be regenerated the next time the code is run.

## Visualization

Example plots showing the difference between the old and new methods can be found in this directory:
- `er_comparison_*.png`: Comparison of ER values with dynamic vs. fixed baselines
- `euel_comparison_*.png`: Comparison of EUEL values with and without nighttime adjustment