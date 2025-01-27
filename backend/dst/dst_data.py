import re
from datetime import date
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta


def fetch_dst_data(year, month):
    base_url = "https://wdc.kugi.kyoto-u.ac.jp"
    urls = [
        f"{base_url}/dst_final/{year:04d}{month:02}/index.html",
        f"{base_url}/dst_provisional/{year:04d}{month:02}/index.html",
        f"{base_url}/dst_realtime/{year:04d}{month:02}/index.html",
    ]
    res = None
    for url in urls:
        try:
            res = requests.get(url)
            if res.status_code == 200:
                break
        except requests.exceptions.RequestException as e:
            print(f"失敗: {url} - {e}")
    if res is None or res.status_code != 200:
        raise Exception("全てのURLでデータ取得に失敗しました")
    soup = BeautifulSoup(res.text, "html.parser")
    pre_data = soup.find("pre")
    if pre_data is None:
        raise Exception("pre要素が見つかりません")

    raw_text = pre_data.get_text()
    raw_data_lines = raw_text.splitlines()
    # データの開始行を特定（DAYの次の）
    data_start = next(
        i for i, line in enumerate(raw_data_lines) if line.strip().startswith("DAY")
    )
    data_lines = raw_data_lines[data_start + 1 :]
    data_array = []
    for line in data_lines:
        if not line.strip():
            continue
        matches = matches = re.findall(r"-?\d+", line)
        if not matches:
            continue
        data_array.append([int(x) for x in matches[1:]])
    return data_array


def is_dst_quiet(dst_index: int):
    return dst_index >= -50


def validate_date_period(start_ym: Tuple[int, int], end_ym) -> None:
    if start_ym[1] < 1 or start_ym[1] > 12:
        raise ValueError("開始年月が不正です")
    if end_ym[1] < 1 or end_ym[1] > 12:
        raise ValueError("終了年月が不正です")
    if start_ym > end_ym:
        raise ValueError("開始年月は終了年月よりも前の日付である必要があります")
    if start_ym < (1963, 1):
        raise ValueError("1963年1月以降のデータしか取得できません")
    if end_ym[0] > date.today().year or (
        end_ym[0] == date.today().year and end_ym[1] > date.today().month
    ):
        raise ValueError("未来のデータは取得できません")


def get_dst_values(start_date: date, end_date: date) -> List[int]:
    dst = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.year == end_date.year and current_date.month == end_date.month:
            days_in_month = end_date.day
        else:
            days_in_month = (current_date + relativedelta(months=1, days=-1)).day
        monthly_dst = fetch_dst_data(current_date.year, current_date.month)
        for day in range(1, days_in_month + 1):
            dst.extend(monthly_dst[day - 1])
        current_date = current_date + relativedelta(months=1)
    return dst


def fetch_disturbued_days(start_ym, end_ym) -> List[date]:
    validate_date_period(start_ym, end_ym)
    disturbance_days = []
    start_date = date(start_ym[0], start_ym[1], 1)
    end_date = date(end_ym[0], end_ym[1], 1)
    current_date = start_date
    while current_date <= end_date:
        monthly_dst = fetch_dst_data(current_date.year, current_date.month)
        for day, day_dst in enumerate(monthly_dst, 1):
            if any(not is_dst_quiet(hour_dst) for hour_dst in day_dst):
                disturbance_days.append(
                    date(current_date.year, current_date.month, day)
                )
        current_date = current_date + relativedelta(months=1)
    return disturbance_days


# start_ym = (2024, 12)
# end_ym = (2025, 1)
# disturbance_days = fetch_disturbance_days(start_ym, end_ym)
# print(len(disturbance_days))
# print(disturbance_days)
