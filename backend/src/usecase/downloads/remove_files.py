import os
import shutil


def remove_files(tmp_dir_path):
    """
    Remove the temporary directory and all its contents.
    
    Args:
        tmp_dir_path: Path to the temporary directory to remove
    """
    if os.path.exists(tmp_dir_path):
        shutil.rmtree(tmp_dir_path)
