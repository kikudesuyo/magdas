import csv
from datetime import timedelta
from typing import List

from src.domain.station_params import Period
from src.service.ee_index.calc_eej_detection import (
    BestEuelSelectorForEej,
    EeIndexStation,
    EejDetection,
    calc_euel_peak_diff,
)


def write_peculiar_eej_to_csv(
    ut_period: Period,
    dip_stations: List[EeIndexStation],
    offdip_stations: List[EeIndexStation],
    path: str,
):
    with open(path, "a", newline="", buffering=1) as f:
        writer = csv.writer(f)
        writer.writerow(["date", "dip_station_code", "offdip_station_code"])
        start_date = ut_period.start.date()
        end_date = ut_period.end.date()
        for current_date in (
            start_date + timedelta(days=i)
            for i in range((end_date - start_date).days + 1)
        ):
            dip_euel_selector = BestEuelSelectorForEej(
                dip_stations, current_date, is_dip=True
            )
            offdip_euel_selector = BestEuelSelectorForEej(
                offdip_stations, current_date, is_dip=False
            )

            dip_euel = dip_euel_selector.select_euel_data()
            offdip_euel = offdip_euel_selector.select_euel_data()

            peak_diff = calc_euel_peak_diff(dip_euel, offdip_euel, current_date)

            eej = EejDetection(peak_diff, current_date)
            if eej.is_peculiar_eej():
                writer.writerow(
                    [
                        current_date,
                        dip_euel.station.code,
                        offdip_euel.station.code,
                    ]
                )


def write_eej_category_to_csv(
    ut_period: Period,
    dip_stations: List[EeIndexStation],
    offdip_stations: List[EeIndexStation],
    path: str,
):
    """EEJのカテゴリをCSVに書き込む



    CSVのフォーマット:
    date, dip_station_code, offdip_station_code, category

    - date: 日付
    - dip_station_code: 採用されたDipステーションのコード
    - offdip_station_code: 採用されたOffDipステーションのコード
    - category: EEJのカテゴリ("peculiar", "normal", "disturbance", "missing")
    """
    with open(path, "a", newline="", buffering=1) as f:
        writer = csv.writer(f)
        writer.writerow(["date", "dip_station_code", "offdip_station_code", "category"])
        start_date = ut_period.start.date()
        end_date = ut_period.end.date()
        for current_date in (
            start_date + timedelta(days=i)
            for i in range((end_date - start_date).days + 1)
        ):
            dip_euel_selector = BestEuelSelectorForEej(
                dip_stations, current_date, is_dip=True
            )
            offdip_euel_selector = BestEuelSelectorForEej(
                offdip_stations, current_date, is_dip=False
            )

            dip_euel = dip_euel_selector.select_euel_data()
            offdip_euel = offdip_euel_selector.select_euel_data()
            peak_diff = calc_euel_peak_diff(dip_euel, offdip_euel, current_date)
            eej = EejDetection(peak_diff, current_date)
            category = eej.eej_category()
            writer.writerow(
                [
                    current_date,
                    dip_euel.station.code,
                    offdip_euel.station.code,
                    category.category,
                ]
            )
            print(f"Processed {current_date} ")
