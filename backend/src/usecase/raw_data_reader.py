import numpy as np
from src.usecase.ee_index.constant.raw_data import (
    EIGHT_COMPONENTS,
    FOUR_COMPONENTS,
    SEVEN_COMPONENTS,
)
from src.usecase.ee_index.constant.time_relation import Min, Sec


def read_raw_min_data(path):
    """
    .mag形式の読み込み

    Arg:
      path (str): .mag形式の絶対パス
    Return:
      data (np.array): 1440分のデータ
    Raises:
      ValueError: データに欠損がある場合
    """
    with open(path, "rb") as file:
        # header情報の除去
        # デリミタ(^Z\00)までがheader
        while True:
            buf = file.read(1)
            if buf == bytes(b"\x1a"):
                buf = file.read(1)
                break
        # 生データの取得
        data = np.fromfile(file, np.float32)
        if len(data) == Min.ONE_DAY.const * SEVEN_COMPONENTS:
            array = data.reshape((Min.ONE_DAY.const, SEVEN_COMPONENTS))
        elif len(data) == Min.ONE_DAY.const * EIGHT_COMPONENTS:
            array = data.reshape((Min.ONE_DAY.const, EIGHT_COMPONENTS))
        else:
            raise ValueError(f"There are missing data! Elements is {len(data)}.")
    return array


def read_raw_sec_data(path):
    """
    .mgdファイルの読み込み

    Arg:
      path (str): .mgdファイルの絶対パス
    Return:
      array (np.array): [[h,d,z,f],[h,d,z,f],...]] (86400, 4) 1 day data per second
    Raises:
      ValueError: データに欠損がある場合
    """
    with open(path, "rb") as file:
        # header情報の除去
        # デリミタ(^Z\00)までがheader
        while True:
            buf = file.read(1)
            if buf == bytes(b"\x1a"):
                buf = file.read(1)
                break
        # 生データの取得
        data = np.fromfile(file, np.float32)
        if len(data) == Sec.ONE_DAY.const * FOUR_COMPONENTS:
            array = data.reshape((Sec.ONE_DAY.const, FOUR_COMPONENTS))
            return array
        else:
            raise ValueError(f"There are missing data! Elements is {len(data)}.")
