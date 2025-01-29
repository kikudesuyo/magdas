import pandas as pd


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
