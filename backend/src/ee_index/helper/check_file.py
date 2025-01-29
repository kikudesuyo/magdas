import os


def is_parent_directory_exist(absolute_path):
    """Check if the directory exist
    Args:
      absolute_path (str):
    Return:
      bool: True if file exist, False otherwise
    """
    parent_directory = os.path.dirname(absolute_path)
    return os.path.isdir(parent_directory)
