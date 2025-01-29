import glob
import io
import os
from zipfile import ZipFile

from src.service.downloads.zip.constant.tmp_path import TMP_DIR_PATH


def create_zip_buffer():
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, "w") as zipf:
        files = glob.glob(os.path.join(TMP_DIR_PATH, "**"))
        for file in files:
            if os.path.isfile(file):
                arcname = os.path.relpath(file, TMP_DIR_PATH)
                zipf.write(file, arcname)
    zip_buffer.seek(0)
    return zip_buffer
