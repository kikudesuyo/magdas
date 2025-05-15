import os
import shutil

from src.utils.path import generate_parent_abs_path

TMP_DIR_PATH = "/tmp"


def remove_tmp_files():
    tmp_dir_path = generate_parent_abs_path(TMP_DIR_PATH)
    shutil.rmtree(tmp_dir_path)
    os.mkdir(tmp_dir_path)
