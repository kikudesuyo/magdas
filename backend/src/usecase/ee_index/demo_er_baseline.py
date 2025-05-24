"""
Demo script to show the ER baseline functionality.

This script demonstrates:
1. How ER values are calculated with fixed baselines
2. How EUEL values are adjusted to make nighttime values closer to 0
"""

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

from src.domain.magdas_station import EeIndexStation
from src.domain.station_params import Period, StationParams
from src.usecase.ee_index.calc_er import Er
from src.usecase.ee_index.calc_h_component import HComponent
from src.usecase.ee_index.er_baseline import ErBaseline
from src.usecase.ee_index.factory_ee import EeFactory
from src.usecase.ee_index.plot_config import PlotConfig


def plot_er_comparison(station, start_date, end_date):
    """Plot a comparison of ER values with and without fixed baselines."""
    period = Period(start_date, end_date)
    params = StationParams(station, period)
    
    # Calculate ER with dynamic baseline (original method)
    h = HComponent(params)
    er_dynamic = Er(h)
    er_dynamic_values = er_dynamic.calc_er(use_fixed_baseline=False)
    
    # Calculate ER with fixed baseline (new method)
    er_fixed = Er(h)
    er_fixed_values = er_fixed.calc_er(use_fixed_baseline=True)
    
    # Plot the results
    PlotConfig.rcparams()
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x_axis = np.arange(0, len(er_dynamic_values), 1)
    ax.plot(x_axis, er_dynamic_values, label="ER (Dynamic Baseline)", color="blue", alpha=0.7)
    ax.plot(x_axis, er_fixed_values, label="ER (Fixed Baseline)", color="red", alpha=0.7)
    
    # Set labels and title
    ax.set_xlabel("Time (minutes)")
    ax.set_ylabel("ER (nT)")
    ax.set_title(f"ER Comparison for {station.code} ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
    ax.legend()
    
    # Show the plot
    plt.tight_layout()
    plt.savefig(f"/workspace/magdas/backend/data/er_baseline/er_comparison_{station.code}.png")
    plt.close()


def plot_euel_comparison(station, start_date, end_date):
    """Plot a comparison of EUEL values with and without nighttime adjustment."""
    period = Period(start_date, end_date)
    params = StationParams(station, period)
    
    # Create factory and components
    factory = EeFactory()
    er = factory.create_er(params)
    edst = factory.create_edst(period)
    euel = factory.create_euel(params)
    
    # Calculate EUEL without adjustment
    euel_values_no_adjust = euel.calc_euel(adjust_nighttime=False)
    
    # Calculate EUEL with adjustment
    euel_values_adjusted = euel.calc_euel(adjust_nighttime=True)
    
    # Get nighttime mask
    nighttime_mask = er.nighttime_mask()
    
    # Plot the results
    PlotConfig.rcparams()
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x_axis = np.arange(0, len(euel_values_no_adjust), 1)
    
    # Plot nighttime background
    for i in range(len(nighttime_mask)):
        if nighttime_mask[i]:
            ax.axvspan(i, i+1, alpha=0.2, color='gray')
    
    ax.plot(x_axis, euel_values_no_adjust, label="EUEL (No Adjustment)", color="blue", alpha=0.7)
    ax.plot(x_axis, euel_values_adjusted, label="EUEL (Nighttime Adjusted)", color="red", alpha=0.7)
    
    # Plot a horizontal line at y=0
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    # Set labels and title
    ax.set_xlabel("Time (minutes)")
    ax.set_ylabel("EUEL (nT)")
    ax.set_title(f"EUEL Comparison for {station.code} ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
    ax.legend()
    
    # Show the plot
    plt.tight_layout()
    plt.savefig(f"/workspace/magdas/backend/data/er_baseline/euel_comparison_{station.code}.png")
    plt.close()


if __name__ == "__main__":
    # Ensure the baseline directory exists
    ErBaseline.ensure_baseline_dir()
    
    # Define the date range and station
    station = EeIndexStation.ANC
    start_date = datetime(2014, 4, 1, 0, 0)
    end_date = datetime(2014, 4, 2, 0, 0)
    
    # Plot ER comparison
    plot_er_comparison(station, start_date, end_date)
    print(f"ER comparison plot saved to /workspace/magdas/backend/data/er_baseline/er_comparison_{station.code}.png")
    
    # Plot EUEL comparison
    plot_euel_comparison(station, start_date, end_date)
    print(f"EUEL comparison plot saved to /workspace/magdas/backend/data/er_baseline/euel_comparison_{station.code}.png")
    
    # Print the baseline values
    baseline_values = ErBaseline.load_baseline_values()
    print("\nER Baseline Values:")
    for date_str, station_values in sorted(baseline_values.items()):
        print(f"  {date_str}:")
        for station_code, value in sorted(station_values.items()):
            print(f"    {station_code}: {value:.2f}")