import os


def is_parent_directory_exist(abs_path):
    """Check if the directory exist
    Args:
      abs_path (str):
    Return:
      bool: True if file exist, False otherwise
    """
    parent_directory = os.path.dirname(abs_path)
    return os.path.isdir(parent_directory)
