import glob
import io
import os
from zipfile import ZipFile


def create_zip_buffer(tmp_dir_path):
    """
    Create a zip file containing all files in the specified temporary directory.
    
    Args:
        tmp_dir_path: Path to the temporary directory containing files to zip
        
    Returns:
        BytesIO: A buffer containing the zip file
    """
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, "w") as zipf:
        files = glob.glob(os.path.join(tmp_dir_path, "**"))
        for file in files:
            if os.path.isfile(file):
                zipf.write(file, arcname=os.path.basename(file))
    zip_buffer.seek(0)
    return zip_buffer
