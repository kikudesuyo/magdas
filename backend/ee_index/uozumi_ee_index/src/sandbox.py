from datetime import datetime, timedelta

import numpy as np
import numpy.ma as ma
from get_pyee import get_py_ee
from matplotlib import pyplot as plt
from read_iaga import get_iaga_ee_for_days
from smoothing import remove_outliers

from util import generate_abs_path


def calculate_correlation(graph1, graph2, window_size):
    correlations = []
    for i in range(0, 1440):
        if i == 1440 - window_size:
            break
        if i < window_size:
            continue
        start_idx = i - window_size
        end_idx = i + window_size + 1
        subset_graph1 = graph1[start_idx:end_idx]
        subset_graph2 = graph2[start_idx:end_idx]
        masked_graph1 = ma.masked_invalid(subset_graph1)
        masked_graph2 = ma.masked_invalid(subset_graph2)
        correlation = ma.corrcoef(masked_graph1, masked_graph2)[0, 1]
        correlations.append(correlation)
    return correlations


def plot_ee_correlation(
    start_datetime, days, absolute_path, index="EDst", station="ANC"
):
    ee = get_iaga_ee_for_days(station, start_datetime, days)
    er, edst, euel = ee
    interpolated_er, interpolated_edst, interpolated_euel = (
        remove_outliers(er),
        remove_outliers(edst),
        remove_outliers(euel),
    )
    py_ee = get_py_ee(station, start_datetime, days)
    # pyedstは既にoutlierを除去している
    py_er, py_edst, py_euel = py_ee
    # 例として、ランダムなデータを生成
    if index == "ER":
        value, py_value = interpolated_er, py_er
    elif index == "EDst":
        value, py_value = interpolated_edst, py_edst
    elif index == "EUEL":
        value, py_value = interpolated_euel, py_euel
    elements = 90
    correlations = calculate_correlation(value, py_value, elements)
    combined_data = np.concatenate((np.array([np.NaN] * elements), correlations))
    combined_data = np.concatenate((combined_data, np.array([np.NaN] * elements)))
    # 結果の表示
    hours = [f"{i:02d}:00" for i in range(0, 25, 3)]
    ticks = np.arange(0, 1441, 180)
    fig, ax = plt.subplots()
    ax.plot(combined_data, color="black", linewidth=2)
    ax.set_xlim(0, 1440)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Time[UT]")
    ax.set_xticks(ticks, labels=hours)
    plt.savefig(absolute_path)
    plt.clf()


def calculate_daily_correlation(date, days, index="EDst", station="ANC"):
    ee = get_iaga_ee_for_days(station, date, days)
    py_ee = get_py_ee(station, date, days)
    er, edst, euel = ee
    interpolated_er = remove_outliers(er)
    interpolated_edst = remove_outliers(edst)
    interpolated_euel = remove_outliers(euel)
    py_er, py_edst, py_euel = py_ee
    if index == "ER":
        value, py_value = interpolated_er, py_er
    elif index == "EDst":
        value, py_value = interpolated_edst, py_edst
    elif index == "EUEL":
        value, py_value = interpolated_euel, py_euel
    # valid_index = ~np.isnan(value) & ~np.isnan(py_value)
    # correlations = np.corrcoef(value[valid_index], py_value[valid_index])[0, 1]
    masked_value = ma.masked_invalid(value)
    masked_py_value = ma.masked_invalid(py_value)
    correlations = ma.corrcoef(masked_value, masked_py_value)[0, 1]
    return correlations


print(calculate_daily_correlation(datetime(2014, 12, 12), 1, "EDst"))
