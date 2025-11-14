import csv
import os
from typing import List

from pydantic import BaseModel, Field


class EejEvent(BaseModel):
    """EEJイベントモデル"""

    region: str = Field(..., description="観測地域名")
    date: str = Field(..., description="イベント日付 (例: '2025-10-14')")
    type: str = Field(
        ..., description="EEJイベントタイプ (例: 'SUDDEN', 'UNDEVELOPED')"
    )


def save_eej_events(events: List[EejEvent], csv_path: str = "eej_events_table.csv"):
    """
    EEJイベントをID付きでCSVに保存
        Args:
            events (list): EEJイベントのリスト (region, date, type を持つオブジェクト)
            csv_path (str, optional): 保存先のCSVファイルパス. Defaults to "eej_events_table.csv".


    eej_events_table.csv
    | カラム名 | 型 | 説明 |
    | --------------- | ----- | ----------------------------------- |
    | id | int | ID (自動採番) |
    | date(1 日値) | str | 日付 (YYYY-MM-DD) |
    | region | str | 地域 |
    | category | str | EEJ のカテゴリ (normal, peculiar, disturbance, missing) |
    """
    # 既存のファイルがある場合は、現在の最大IDを確認
    if os.path.exists(csv_path):
        with open(csv_path, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            existing_rows = list(reader)
            last_id = int(existing_rows[-1]["id"]) if existing_rows else 0
    else:
        existing_rows = []
        last_id = 0

    # 追記するデータを整形
    new_rows = []
    for i, event in enumerate(events, start=1):
        new_rows.append(
            {
                "id": last_id + i,
                "region": event.region,
                "date": event.date,
                "type": event.type,
            }
        )

    # 書き込み（新規 or 追記）
    write_header = not os.path.exists(csv_path)
    with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "region", "date", "type"])
        if write_header:
            writer.writeheader()
        writer.writerows(new_rows)
