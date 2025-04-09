import glob
import io
import os
from zipfile import ZipFile

from src.service.downloads.constant.tmp_path import TMP_DIR_PATH
from src.utils.path import generate_parent_abs_path


def create_zip_buffer():
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, "w") as zipf:
        tmp_dir_path = generate_parent_abs_path(TMP_DIR_PATH)
        files = glob.glob(os.path.join(tmp_dir_path, "**"))
        for file in files:
            if os.path.isfile(file):
                arcname = os.path.relpath(file, TMP_DIR_PATH)
                zipf.write(file, arcname)
    zip_buffer.seek(0)
    return zip_buffer
