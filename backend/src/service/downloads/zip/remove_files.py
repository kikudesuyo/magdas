import os
import shutil

from src.service.downloads.constant.tmp_path import TMP_DIR_PATH


def remove_files():
    shutil.rmtree(TMP_DIR_PATH)
    os.mkdir(TMP_DIR_PATH)
