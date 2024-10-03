import pandas as pd
from features.downloads.iaga.meta_data import get_meta_data

data = {
    "DATE": ["2015-03-19", "2015-03-19", "2015-03-19", "2015-03-19"],
    "TIME": ["00:00:00.000", "00:01:00.000", "00:02:00.000", "00:03:00.000"],
    "DOY": [78, 78, 78, 78],
    "EDst1h": [-87.86, -87.99, -88.20, -88.40],
    "EDst6h": [-80.90, -80.88, -80.87, -80.86],
    "ER": [-106.21, -106.40, -106.57, -106.46],
    "EUEL": [-25.31, -25.51, -25.70, -25.61],
}

meta_data = get_meta_data("Huancayo", "HUA", -12.000, 284.710, 8888.88)


def save_iaga_format(meta_data, data, file_name):
    df = pd.DataFrame(data)
    with open(f"{file_name}.txt", "w") as f:
        # メタデータ
        for key, value in meta_data.items():
            f.write(f"{key:<25} {value:<40}\n")
        # ッダー
        f.write(
            f"{'DATE':<11}{'TIME':<13}{'DOY':<7}{'EDst1h':<10}{'EDst6h':<10}{'ER':<10}{'EUEL':<10}\n"
        )
        # データ
        for _, row in df.iterrows():
            f.write(
                f"{row['DATE']:<11}{row['TIME']:<13}{str(row['DOY']).zfill(3):<7}{row['EDst1h']:<10.2f}{row['EDst6h']:<10.2f}{row['ER']:<10.2f}{row['EUEL']:<10.2f}\n"
            )


# データを保存
save_iaga_format(meta_data, data, "test")
