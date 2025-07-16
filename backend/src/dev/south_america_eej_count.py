import pandas as pd
from src.utils.path import generate_parent_abs_path


def count_categories(csv_path, start_date=None, end_date=None):
    """
    CSVファイルから指定された期間内のカテゴリごとの出現回数をカウントします。

    Args:
        csv_path (str): CSVファイルのパス。
        start_date (str, optional): 開始日 (YYYY-MM-DD)。Defaults to None.
        end_date (str, optional): 終了日 (YYYY-MM-DD)。Defaults to None.

    Returns:
        dict: カテゴリをキー、出現回数を値とする辞書。
    """
    try:
        # CSVを読み込む
        df = pd.read_csv(csv_path, parse_dates=["date"])
    except FileNotFoundError:
        print(f"Error: The file was not found at {csv_path}")
        return {}

    # 期間でフィルタリング
    if start_date:
        df = df[df["date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["date"] <= pd.to_datetime(end_date)]

    # カテゴリごとの出現回数を計算
    total = len(df)
    if total == 0:
        return {}

    counts = df["category"].value_counts()
    return counts.to_dict()


if __name__ == "__main__":
    # 例: 2015-01-01 から 2015-01-10 まで
    path = generate_parent_abs_path("/src/dev/south_america_eej_category.csv")
    start_date = "2014-01-01"
    end_date = "2020-12-31"

    counts = count_categories(path, start_date, end_date)

    if counts:
        print(f"Category Counts ({start_date} to {end_date}):")
        for category, count in counts.items():
            print(f"  - {category}: {count}")
    else:
        print(f"No data available in the specified date range for {path}.")
