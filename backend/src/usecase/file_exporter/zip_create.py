import glob
import io
import os
from zipfile import ZipFile


def create_zip_buffer(dir_path: str) -> io.BytesIO:
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, "w") as zipf:
        files = glob.glob(os.path.join(dir_path, "**"))
        for file in files:
            if os.path.isfile(file):
                zipf.write(file, arcname=os.path.basename(file))
    zip_buffer.seek(0)
    return zip_buffer
