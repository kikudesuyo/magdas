import os
import shutil

from src.usecase.downloads.tmp_path import TMP_DIR_PATH
from src.utils.path import generate_parent_abs_path


def remove_files():
    tmp_dir_path = generate_parent_abs_path(TMP_DIR_PATH)
    shutil.rmtree(tmp_dir_path)
    os.mkdir(tmp_dir_path)
